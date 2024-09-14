import numpy as np
from Grid import Grid
from Raster import RasterF

import pickle
from pathlib import Path

path = str(Path.home()) + '\\Desktop\\Test'
sp,ep,grp_map,ts=pickle.load(open(path+'\\output.dat','rb'))

etp=QgsProject.instance().mapLayersByName('etp_temp')[0]
es=rfe.features_to_ij_and_info(list(etp.getFeatures()),blocke)
ep=es[0][0]


#ep=np.array([617,86])
print(ep)
grp=Grid(grp_map)
collect=np.array([ep])
while (ep!=sp).any():
    pp=grp.value(ep)
    collect=np.insert(collect,len(collect),pp,axis=0)
    ep=pp

points=rfe.ijs_to_points(collect)
geo=RasterF.create_path_feature_from_points(points,0)
geo.setAttributes([1])
loc=r'C:\Users\SANJEEV BASHYAL\Documents\QGIS\Test\after_tunnel_1.shp'
fields=QgsFields()
fields.append(QgsField('id',QVariant.Int))
writer=QgsVectorFileWriter(loc,'UTF-8',fields,QgsWkbTypes.LineString,QgsCoordinateReferenceSystem('ESRI:102306'),'ESRI Shapefile')
writer.addFeature(geo)
del(writer)
iface.addVectorLayer(loc,'','ogr')

#pickle.dump(collect,open(r'C:/Users/SANJEEV BASHYAL/Documents/QGIS/Grade Path/least_grade_distance_path.dat','wb'))