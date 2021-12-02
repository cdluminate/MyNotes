import numpy as np
prior = np.array([0.5, 0.5])
likely = np.array([[0.4,0.05,0.05,0.05,0.05,0.4],  [0.3,0.3,0.1,0.1,0.1,0.1]])
observe = np.array([6,4,5,1,2,3,4,5,2,2,1,4,3,4,6,2,1,6])

for m in range(10):
    post = np.zeros([2, len(observe)])
    for i, o in enumerate(observe):
        c0 = prior[0] * likely[0, o-1]
        c1 = prior[1] * likely[1, o-1]
        post[0,i] = c0 / (c0 + c1)
        post[1,i] = c1 / (c0 + c1)
        s = post.sum(axis=1)
    print(post)
    print(post.sum(axis=1))
    for o in range(6):
        likely[0,o] = post[0,np.argwhere(observe == o+1)].sum()/s[0]
        likely[1,o] = post[1,np.argwhere(observe == o+1)].sum()/s[1]
    print(likely)
    prior = s / s.sum()
    print(prior)
