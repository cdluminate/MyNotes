# https://www.zhihu.com/question/66988664
# http://pytorch.org/docs/master/nn.html
# https://github.com/andreasveit/triplet-network-pytorch

import torch as th
import torch.nn.functional as F

'''
torch function note:

    1. torch.nn.functional.pairwise_distance(in1, in2, p=2)
       fn : in1:(N, D) x in2:(N, D) -> out:(N, 1)
       N batchsize, D emb dimension.
       out[i,:] is distance between in1[i,:] and in2[i,:].
       the "distance" (e.g. torch.dist()) is the p-norm of in1-in2.

    2. MarginRankingLoss, Euclidean
       loss(x1, x2, y) = max(0, margin - y * (x1 - x2))
       torch/nn/_functions/loss.py
'''

class TripletLoss(th.nn.Module):
    def __init__(self, t1, t2, beta):
        super(TripletLoss, self).__init__()
        self.t1 = t1 # repulsion margin
        self.t2 = t2 # attraction margin
        self.beta = beta # importance coef of the attraction part
    def forward(self, anchor, positive, negative):
        # ap_i = dist(a_i, p_i)
        matched = th.pow(F.pairwise_distance(anchor, positive), 2)
        # an_i = dist(a_i, n_i)
        mismatched = th.pow(F.pairwise_distance(anchor, negative), 2)
        # ap_i + alpha > an_i --- alpha + ap_i - an_i > 0 --- hinge
        # repulsion part, p_r = max(0, t1 + ap_i - an_i)
        part_r = th.clamp(self.t1 + matched - mismatched, min=.0)
        # attraction part, p_a = max(t2, ap_i)
        part_a = th.clamp(matched, min=self.t2)
        # total hinge loss = p_r + β p_a
        losses = part_r + self.beta * part_a
        loss = th.mean(losses)
        return loss
