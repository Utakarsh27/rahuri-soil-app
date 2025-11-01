
// -----------------------------------------------------------
// SIMPLE SOIL SALINITY & SLOPE ANALYSIS (MPKV RAHURI)
// -----------------------------------------------------------

// 1️⃣ Study Area
var area = ee.Geometry.Polygon([
  [[74.600,19.420],
   [74.650,19.420],
   [74.650,19.390],
   [74.600,19.390]]
]);
var area = ee.Geometry.Polygon([...]);
Map.centerObject(area, 13);
Map.addLayer(area, {color:'red'}, 'Study Area');

// 2️⃣ Sentinel-2 Imagery (Cloud-filtered Composite)
var s2 = ee.ImageCollection('COPERNICUS/S2_SR')
  .filterBounds(area)
  .filterDate('2024-01-01', '2024-12-31')
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
  .select(['B2','B3','B4','B8','B11','B12']); // essential bands only

// Take median composite (auto-cloud reduced)
var s2_median = s2.median().clip(area);
Map.addLayer(s2_median, {bands:['B4','B3','B2'], min:0, max:0.3}, 'True Color');

// 3️⃣ Indices for Salinity
var ndvi = s2_median.normalizedDifference(['B8','B4']).rename('NDVI');
var ndwi = s2_median.normalizedDifference(['B3','B8']).rename('NDWI');

// Simple salinity indicator: low NDVI + low NDWI
var salinity = ndvi.multiply(-1).add(1).add(ndwi.multiply(-1).add(1)).divide(2);
Map.addLayer(salinity, {min:0, max:1, palette:['green','yellow','red']}, 'Salinity Index');

// 4️⃣ Slope from SRTM DEM
var dem = ee.Image('USGS/SRTMGL1_003').clip(area);
var slope = ee.Terrain.slope(dem);
Map.addLayer(slope, {min:0, max:20, palette:['lightgreen','yellow','red']}, 'Slope');

// -----------------------------------------------------------
// Optional: Export Maps
Export.image.toDrive({
  image: salinity,
  description: 'Rahuri_Salinity_Index',
  region: area,
  scale: 10,
  maxPixels: 1e13
});

Export.image.toDrive({
  image: slope,
  description: 'Rahuri_Slope',
  region: area,
  scale: 30,
  maxPixels: 1e13
});
// -----------------------------------------------------------
// EXPORT VISUALIZED MAPS AS PNG (for poster / demo)
// -----------------------------------------------------------

// Visualization styles
var salVis = {min: 0, max: 1, palette: ['green','yellow','red']};
var slopeVis = {min: 0, max: 20, palette: ['lightgreen','yellow','red']};

// Visualize before export (to keep legend colors)
var salinity_vis = salinity.visualize(salVis);
var slope_vis = slope.visualize(slopeVis);

// Export salinity map
Export.image.toDrive({
  image: salinity_vis,
  description: 'Rahuri_Salinity_Map_PNG',
  folder: 'GEE_exports',
  fileNamePrefix: 'salinity_map_rahuri',
  scale: 10,
  region: area,
  maxPixels: 1e13
});

// Export slope map
Export.image.toDrive({
  image: slope_vis,
  description: 'Rahuri_Slope_Map_PNG',
  folder: 'GEE_exports',
  fileNamePrefix: 'slope_map_rahuri',
  scale: 30,
  region: area,
  maxPixels: 1e13
});