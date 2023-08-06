import torch
import numpy
import sqlite3
import numba
import extensions
import pepid_utils
import blackboard
import pickle
import msgpack
import tqdm
import copy

inited = False

@numba.njit(locals={'max_mz': numba.int32, 'mult': numba.float32, 'corr': numba.float32, 'sqr_ml': numba.float32, 'sqr_blit': numba.float32, 'mlspec': numba.float32[:,::1], 'blit': numba.float32[::1]})
def correlate_spectra(blit, mlspec, max_mz, mult):
    corr = 0
    sqr_ml = 0
    sqr_blit = 0
    for mz, intens in mlspec:
        mzidx = int(mz)
        if mzidx >= max_mz / mult:
            break
        blit_int = blit[mzidx]
        corr += blit_int * intens
        sqr_ml += intens**2
        sqr_blit += blit_int**2
    corr /= (numpy.sqrt(sqr_blit) * numpy.sqrt(sqr_ml) + 1e-10)

    return corr

def specgen_features(header, lines):
    print("XXX")
    import sqlite3

    batch_size = blackboard.config['pin.specgen_features'].getint('batch size')

    cand_file = blackboard.DB_PATH + "_cands.sqlite"
    qfile = blackboard.DB_PATH + "_q.sqlite"

    if __package__ is None or __package__ == '':
        from ml import specgen
    else:
        from .ml import specgen

    conn = sqlite3.connect(cand_file)
    connq = sqlite3.connect(qfile)
    conn.row_factory = sqlite3.Row
    connq.row_factory = sqlite3.Row
    cur = conn.cursor()
    curq = connq.cursor()

    ret = []

    for i in tqdm.tqdm(range(0, len(lines), batch_size)):
        the_lines = lines[i:i+batch_size]
        cands = [l[header.index('candrow')] for ll in the_lines for l in ll]
        quers = [l[header.index('qrow')] for ll in the_lines for l in ll]
        cur.execute("SELECT rowid, * FROM candidates WHERE rowid IN ({}) ORDER BY rowid;".format(",".join(cands)))
        curq.execute("SELECT rowid, * FROM queries WHERE rowid in ({}) ORDER BY rowid;".format(",".join(quers)))
        allcands = cur.fetchall()
        allqs = curq.fetchall()
        extras = {r['rowid'] : (r['seq'], msgpack.loads(r['mods']), {k:v for k, v in dict(r).items() if k not in ['meta', 'data', 'spec']}) for r in allcands}
        specs = {r['rowid'] : numpy.asarray(pickle.loads(r['spec']), dtype='float32') for r in allqs}
        print(list(specs.keys()))
        if i == 0:
            print(lines[0][0], dict(extras[int(lines[0][0][header.index('candrow')])][-1]))

        for iql, query_lines in enumerate(lines[i:i+batch_size]):
            if len(query_lines) == 0:
                break
            ret.append([])
            for iline, line in enumerate(query_lines):
                charge = int(line[header.index('query_charge')])-1
                spec = specs[int(line[header.index('qrow')])]
                blit = prepare_spec(spec)
                #blit = pepid_utils.blit_spectrum(spec, specgen.PROT_TGT_LEN, 0.1)
                mlspec = extras[int(line[header.index('candrow')])]
                mlspec = post_ml_spectrum([{'seq': mlspec[0], 'mods': mlspec[1], 'meta': {}}])
                mlspec = mlspec[0]['meta']['MLSpec'][min(charge, specgen.MAX_CHARGE-1)]
                if iql == 0 and iline < 10:
                    print(spec[:,0].min(), spec[:,0].max(), spec[:,1].min(), spec[:,1].max(), blit.min(), blit.max(), charge, mlspec[:,0].min(), mlspec[:,0].max(), mlspec[:,1].min(), mlspec[:,1].max())

                #blitspec = copy.deepcopy(mlspec_raw)
                #mlspec_raw = pepid_utils.dense_to_sparse(mlspec_raw.reshape((1, *mlspec_raw.shape)), n_max=2000).reshape((2000, 2))
                #mlspec[:,0] *= 0.1
                #blitspec = specgen.prepare_spec(mlspec)
                #blitspec = pepid_utils.blit_spectrum(mlspec, specgen.PROT_TGT_LEN, 0.1)
                #corr = ((blitspec / (numpy.linalg.norm(blitspec) + 1e-10)) * (blit / (numpy.linalg.norm(blit) + 1e-10))).sum()
                corr = correlate_spectra(blit, mlspec, specgen.MAX_MZ, 0.1)
                ret[-1].append({'MLCorr': corr})
    return ret

def make_inputs(seqs, seqmods):
    from ml import specgen
    th_spec = numpy.zeros((len(seqs), specgen.PROT_TGT_LEN, 5+1), dtype='float32')
    for i, (seq, mods) in enumerate(zip(seqs, seqmods)):
        all_masses = []

        for z in range(1, 6):
            masses = numpy.asarray(pepid_utils.theoretical_masses(seq, mods, nterm=NTERM, cterm=CTERM, exclude_end=True), dtype='float32').reshape((-1,2))
            th_spec[i,:,z-1] = pepid_utils.blit_spectrum(masses, specgen.PROT_TGT_LEN, 0.1)

        mass = pepid_utils.neutral_mass(seq, mods, nterm=NTERM, cterm=CTERM, z=1)
        th_spec[i,min(specgen.PROT_TGT_LEN-1, int(numpy.round(mass / 0.1))),5] = 1

    return th_spec

def make_input(seq, mods):
    return make_inputs([seq], [mods])[0]

@numba.njit()
def prepare_spec(spec):
    spec_fwd = pepid_utils.blit_spectrum(spec, specgen.PROT_TGT_LEN, 0.1)
    spec_fwd = numpy.sqrt(spec_fwd)

    return spec_fwd

MODEL = None
class post_ml_spectrum(object):
    required_fields = {'candidates': ['seq', 'mods', 'meta']}

    def __new__(cls, cands):
        if __package__ is None or __package__ == '':
            from ml import specgen
        else:
            from .ml import specgen
        import torch

        batch_size = blackboard.config['processing.db.post_ml_spectrum'].getint('batch size')
        device = blackboard.config['processing.db.post_ml_spectrum']['device']
        if device is None:
            device = 'cpu'

        if 'cuda' in device:
            blackboard.lock()
            gpu_lock = blackboard.acquire_lock(device)

            blackboard.lock(gpu_lock)

            blackboard.unlock()

        global MODEL

        if MODEL is None:
            MODEL = specgen.Model().eval().to(device)
            MODEL.load_state_dict(torch.load("ml/best_specgen.pkl", map_location=device))

        cterm = blackboard.config['processing.db'].getfloat('cterm cleavage')
        nterm = blackboard.config['processing.db'].getfloat('nterm cleavage')

        seqs = []
        mods = []
        for c in cands:
            seqs.append(c['seq'])
            mods.append(c['mods'])
        embs = torch.FloatTensor(make_inputs(seqs, mods))

        max_peaks = 2000
        out = [None for _ in range(len(embs))]

        with torch.no_grad():
            for bidx in range(0, len(embs), batch_size):
                pred = MODEL(embs[bidx:bidx+batch_size].to(device))
                sparsy = (pred * (pred >= 1e-3)).detach().cpu().numpy()
                sparsed = pepid_utils.dense_to_sparse(sparsy.reshape((-1, sparsy.shape[-1])), n_max = max_peaks)
                sparsed = sparsed.reshape((-1, sparsy.shape[1], sparsed.shape[-2], 2))
                out[bidx:bidx+batch_size] = sparsed

        for o in range(len(out)):
            cands[o]['meta'] = {'MLSpec': out[o]}
        return cands

NTERM = 0
CTERM = 0
def init():
    blackboard.config.read("data/default.cfg")
    blackboard.config.read("massive.cfg")
    blackboard.setup_constants()
    blackboard.LOCK = blackboard.acquire_lock()
    global NTERM
    global CTERM
    NTERM, CTERM = blackboard.config['processing.db'].getfloat('nterm cleavage'), blackboard.config['processing.db'].getfloat('cterm cleavage')
    global inited
    inited = True
    global specgen
    from ml import specgen

def run():
    if not inited:
        init()
    from ml import specgen

    in_fname = blackboard.config['data']['output']
    fname, fext = in_fname.rsplit('.', 1)
    suffix = blackboard.config['rescoring']['suffix']
    pin_name = fname + suffix + "_pin.tsv"

    fin = open(in_fname, 'r')
    header = next(fin).strip().split("\t")
    title_idx = header.index("title")

    lines = []
    cnt = -1
    prev = None
    start = 0
    end = 250
    for il, l in enumerate(fin):
        line = l.strip().split("\t")
        if line[title_idx] != prev:
            prev = line[title_idx]
            cnt += 1
            if cnt < start:
                continue
            if cnt >= end:
                break
            lines.append([])
        if start <= cnt < end:
            lines[-1].append(l.strip().split("\t"))

    fin.close()

    pin_header = pepid_utils.generate_pin_header(header, lines[0][0])
    pin_lines = pepid_utils.tsv_to_pin(header, lines, start)
    corrs = []
    retlines = []
    for l in pin_lines:
        corrs.append([float(ll[pin_header.index('MLCorr')]) for ll in l])
        retlines.append([ll for ll in l])

    return retlines, corrs
