import numpy as np
from Grid import Grid

import pickle
from pathlib import Path

path = str(Path.home()) + "\\Desktop\\Test"
gr_map, sp, ep, srd_map, srn_map, sru_map = pickle.load(open(path + "\\dump.dat", "rb"))
sp = np.array(sp)
osp = sp.copy()
ep = np.array(ep)
gr = Grid(gr_map)
csrd = Grid(srd_map)
csrn = Grid(srn_map)
csru = Grid(sru_map)

del (srd_map, srn_map, sru_map, gr_map)
grd = Grid(np.full([gr.h, gr.w], np.inf))  # stores least distances
grp = Grid(np.full([gr.h, gr.w], None))  # save path in form of points list

# sp=np.array(ss[0][0]);tsp=np.array(rfe._row_col_to_point_list(sp))
# ep=np.array(es[0][0]);tep=np.array(rfe._row_col_to_point_list(ep))

grd.insert(0, sp)
grp.insert(sp, sp)
sz = 6000
get_nei = np.full([sz, 2], -1)
get_nei[0] = sp
c_pp = np.full([sz, 2], -1)
c_length = np.full([sz], np.inf)
locate = 0
locatelist = []
if csrn.value(sp).size != 0:
    c_pp[locate] = csrn.value(sp)[0]
    c_length[locate] = csrd.value(sp)[0] + grd.value(sp)
    locate = locate + 1
else:
    print("Starting point has no neighbors")
    exit(0)


snei = csru.neighbors_ext(sp)
for point in snei:
    ppd = csrd.value(point)
    nein = csrn.value(point)
    pindex = np.where((nein == sp).all(1))[0]
    if pindex.size == 0:
        continue
    ppd = np.delete(ppd, pindex)
    nein = np.delete(nein, pindex, axis=0)
    if nein.size == 0:
        index0 = np.where((get_nei == point).all(1))[0]
        if index0.size > 0:
            get_nei[index0] = [-1, -1]
            c_pp[index0] = [-1, -1]
            c_length[index0] = np.inf
            locatelist.append(index0[0])
        csru.insert(None, point)
    csrd.insert(ppd, point)
    csrn.insert(nein, point)


# collect=np.array([sp])
i = 1
psp = sp
while (sp!=ep).any():
    print(i)
    index = np.argmin(c_length[0:locate])
    pp = c_pp[index].copy()
    if (pp == np.array([-1, -1])).all():
        print("No further search possible; Reached sink or peak")
        break
    grd.insert(c_length[index], pp)
    grp.insert(get_nei[index].copy(), pp)

    if csrn.value(pp).size != 0:
        if locatelist:
            location = locatelist[0]
            locatelist.pop(0)
        else:
            location = locate
            locate = locate + 1
        get_nei[location] = pp
        c_pp[location] = csrn.value(pp)[0]
        c_length[location] = csrd.value(pp)[0] + grd.value(pp)

    while True:
        c_pp_array = csrn.value(get_nei[index])
        c_length_array = csrd.value(get_nei[index])
        if len(c_pp_array) > 1:
            c_pp[index] = c_pp_array[1]
            c_length[index] = c_length_array[1] + grd.value(get_nei[index])
        else:
            csru.insert(None, get_nei[index])
            get_nei[index] = [-1, -1]
            c_pp[index] = [-1, -1]
            c_length[index] = np.inf
            locatelist.append(index)

        indexes = np.where((c_pp == pp).all(1))[0]
        if indexes.size == 0:
            break
        else:
            index = indexes[0]

    snei = csru.neighbors_ext(pp)
    for point in snei:
        ppd = csrd.value(point)
        nein = csrn.value(point)
        pindex = np.where((nein == pp).all(1))[0]
        if pindex.size == 0:
            continue
        ppd = np.delete(ppd, pindex)
        nein = np.delete(nein, pindex, axis=0)
        if nein.size == 0:
            index1 = np.where((get_nei == point).all(1))[0]
            if index1.size > 0:
                get_nei[index] = [-1, -1]
                c_pp[index] = [-1, -1]
                c_length[index] = np.inf
                locatelist.append(index1[0])
            csru.insert(None, point)

        csrd.insert(ppd, point)
        csrn.insert(nein, point)

    # print(i,pp)
    psp = sp
    sp = pp
    # collect=np.insert(collect,len(collect),pp,axis=0)

    i = i + 1

    if i > 4000000:
        break

pickle.dump([osp, ep, grp.map, grd.map], open(path + "\\output.dat", "wb"))

