import blackboard
blackboard.config.read('data/default.cfg')
blackboard.config.read('massive.cfg')
blackboard.setup_constants()
blackboard.LOCK = blackboard.acquire_lock()

import pepid_utils
import extensions
import re

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

import msgpack

import numpy
import tables
import pickle

import tqdm

import os
import sys

CUDA = True

BATCH_SIZE = 16
MAX_SIZE = 50000

INIT_PATIENCE = 999

#raw_data = tables.open_file("yeast.h5", 'r')
import sqlite3

from ml.specgen import *

class MsDataset(Dataset):
    def __init__(self, max_charge=MAX_CHARGE, epoch_len=None, theoretical=True, generated=False, shuffle=False):
        self.conn = sqlite3.connect('/scratch/zumerj/tmp/pepidrun_massive/human_cands.sqlite')
        self.qconn = sqlite3.connect('/scratch/zumerj/tmp/pepidrun_massive/human_q.sqlite')
        self.conn.row_factory = sqlite3.Row
        self.qconn.row_factory = sqlite3.Row
        self.curr = self.conn.cursor()
        self.qcurr = self.qconn.cursor()

        f = open('pepid_res_massive.tsv', 'r')
        self.header = next(f).strip().split('\t')
        self.lines = list(map(lambda x: x.strip().split('\t'), f))

        self.len = 50000
        self.max_charge = max_charge

    def __len__(self):
        return self.len

    def __getitem__(self, idx):
        line = self.lines[idx % len(self.lines)]
        cand = line[int(self.header.index('candrow'))]
        quer = line[int(self.header.index('qrow'))]
        self.curr.execute("SELECT seq, mods FROM candidates WHERE rowid = ?;", (cand,))
        c = self.curr.fetchone()
        self.qcurr.execute("SELECT charge, spec FROM queries WHERE rowid = ?;", (quer,))
        q = self.qcurr.fetchone()
        charge = q['charge']

        seq = c['seq']
        mods = msgpack.loads(c['mods'])

        spec = numpy.asarray(pickle.loads(q['spec']), dtype='float32')

        all_masses = []
        th_spec = make_input(seq, mods)
        #for z in range(1, 6):
        #    all_masses.append(numpy.asarray(pepid_utils.theoretical_masses(seq, mods, nterm=1.007825, cterm=17.002735, charge=z, exclude_end=True)).reshape((-1,2))[:,0])

        #    #print(rawseq, seq, mods, charge, len(seq), len(mods))
        #    th_spec = numpy.zeros((PROT_TGT_LEN, 5+1), dtype='float32')
        #    for z in range(len(all_masses)):
        #        for mz in sorted(all_masses[z]):
        #            if int(numpy.round(mz / SIZE_RESOLUTION_FACTOR)) < PROT_TGT_LEN:
        #                th_spec[int(numpy.round(mz / SIZE_RESOLUTION_FACTOR)), z] += 1
        #            else:
        #                break
        #        th_spec[:,z] /= (th_spec[:,z].max() + 1e-10)

        #mass = pepid_utils.neutral_mass(seq, mods, nterm=1.007825, cterm=17.002735, z=1)
        #th_spec[min(PROT_TGT_LEN-1, int(numpy.round(mass / SIZE_RESOLUTION_FACTOR))),5] = 1
#        #mass = (self.data.root.meta[self.idxs[idx]]['mass'] * charge) - (charge * pepid_utils.MASS_PROT)
#        #th_spec[:,5+charge-1] = 1.
#        #th_spec[:,5+5] = mass / 5000.
#
#        spec_fwd = numpy.zeros((PROT_TGT_LEN,))
#        for mz, intens in spec:
#            #jitter = (numpy.random.rand() * 2 - 1) * 5 * 1e-6 * mz
#            jitter = 0
#            idx = int(numpy.round((mz + jitter) / SIZE_RESOLUTION_FACTOR))
#            if idx < PROT_TGT_LEN:
#                spec_fwd[idx] += intens
#            else:
#                break
#        spec_fwd = spec_fwd / (spec_fwd.max() + 1e-10)
#        spec_fwd = numpy.sqrt(spec_fwd)


        spec_fwd = prepare_spec(spec)
        mass = pepid_utils.neutral_mass(seq, mods, nterm=1.007825, cterm=17.002735, z=1)

        enc_seq = th_spec
          
        out_set = []
        out_set.append(torch.FloatTensor(enc_seq))
        out_set.append(torch.LongTensor([charge-1])) # 0-index the charge...
        out_set.append(torch.FloatTensor([mass]))
        out_set.append(torch.FloatTensor(spec_fwd))
        #out_set[-1] = torch.sqrt(out_set[-1])
        return tuple(out_set)

def make_run():
    model = Model()

    if CUDA:
        torch.backends.cudnn.enabled = True
        model.cuda()

    print(model)
    model.load_state_dict(torch.load("ml/best_specgen.pkl"))

    numpy.random.seed(0)

    dataset = MsDataset(epoch_len=None)
    dataset_test = dataset
    dl = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=0, drop_last=True)
    dl_test = DataLoader(dataset_test, batch_size=BATCH_SIZE, shuffle=True, num_workers=0, drop_last=True)

    loss_fn = torch.nn.CosineSimilarity(dim=-1).cuda() #torch.nn.MSELoss().cuda()
    #loss_fn = torch.nn.MSELoss().cuda()
    nll_loss = torch.nn.NLLLoss().cuda()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    patience = INIT_PATIENCE
    best_loss = float('inf')
    last_epoch = 200
    epoch_idx = 0

    prev_sim = 0

    while epoch_idx < last_epoch and patience > 0:
        loss_value = {'train': 0, 'test': 0}
        cos_sim = {'train': 0, 'test': 0}
        sparsity = {'train': 0, 'test': 0}
        mass_delta = {'train': 0, 'test': 0}
        charge_acc = {'train': 0, 'test': 0}

        for this_dl in (dl, dl_test):
            phase = 'train' if this_dl is dl else 'test'
            if this_dl is dl:
                model.train()
            else:
                model.eval()
            n = 0
            bar = tqdm.tqdm(enumerate(this_dl), total=len(this_dl))
            for it, batch in bar:
                seq, charge, mass, spec = batch
                seq = seq.cuda()
                spec = spec.cuda()
                mass = mass.view(-1).cuda()
                charge = charge.view(-1).long().cuda()

                spec = spec.view(-1, spec.shape[-1])
                with torch.no_grad():
                    pred = model(seq)

                pred_select = torch.stack([pred[i,charge[i],:] for i in range(pred.shape[0])])
                pred_select_sparse = (pred_select * (pred_select > 1e-3)).detach().cpu().numpy()
                spec = spec.detach().cpu().numpy()
                #l_expr = -loss_fn(pred_select_sparse, spec[:,:PROT_TGT_LEN]).mean() - loss_fn(pred_select, spec[:,:PROT_TGT_LEN]).mean()
                #l_expr = -loss_fn(pred_select_sparse, spec[:,:PROT_TGT_LEN]).mean() #+ nll_loss(pred_charge, charge) + ((pred_mass - (mass/5000))**2).mean()
                pred_sparse = pepid_utils.dense_to_sparse(pred_select_sparse.reshape((-1, pred_select_sparse.shape[-1])), n_max=2000).reshape((-1, 2000, 2))
                l_expr = numpy.hstack([extensions.correlate_spectra(s[:PROT_TGT_LEN], p, PROT_TGT_LEN, 0.1) for s, p in zip(spec, pred_sparse)]).mean()

                #loss_value[phase] += l_expr.data.cpu().numpy()
                loss_value[phase] += l_expr #.data.cpu().numpy()
                #spec_post = spec[:,:PROT_TGT_LEN] / (torch.norm(spec[:,:PROT_TGT_LEN], p=2, dim=-1, keepdim=True) + 1e-10)
                #pred_post = pred_select / (torch.norm(pred_select, p=2, dim=-1, keepdim=True) + 1e-10)
                #cos_sim[phase] += (spec_post * pred_post).sum(dim=-1).mean().detach().cpu().numpy()
                #charge_acc[phase] += (pred_charge.argmax(dim=-1) == charge).float().mean()
                #mass_delta[phase] += torch.abs(pred_mass - (mass/5000)).mean()

                #sparsity[phase] += (pred_select_sparse / (pred_select_sparse + 1e-10)).mean()

                n += 1

                bar.set_description("[{}] {}: {:.3f} -> L:{:.3f} S:{:.3f} C:{:.3f} M:{:.3f}".format(epoch_idx, "T{}ing".format(phase[1:]), cos_sim[phase] / max(n, 1), loss_value[phase] / max(n, 1), sparsity[phase] / max(n, 1), charge_acc[phase] / max(n, 1), mass_delta[phase] / max(n, 1)))

            loss_value[phase] /= n
            cos_sim[phase] /= n
            sparsity[phase] /= n
            mass_delta[phase] /= n
            charge_acc[phase] /= n

        prev_sim = cos_sim['test']

        epoch_idx += 1

if __name__ == '__main__':
    make_run()
