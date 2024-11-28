# (2024)Crawling Baidu Street View data  
Including historical Baidu Street View data(包括百度街景历史数据)
  
Project Information: crawl Baidu Street View according to geospatial coordinates (crawl all Baidu Street View data in the current coordinate position)  
Project Benefits: can crawl Baidu Street View data  
Project Details: This project searches for Baidu Street View historical data and latest data by traversing geospatial coordinates one by one.  
Code to use the premise:
1. Prepare your own geospatial coordinates data, the data should be csv (UTF-8) format, while using the geographic coordinate system;  
2. If your data is not in csv (UTF-8) format, you can convert your data to that format, for example: shp data imported as csv format data, and use notepad software to convert it to csv (UTF-8) format;  
3. In order to further improve the efficiency of streetscape crawling, users can extract the building footprint data, the use of building footprint data (building footprint data) is a simple idea: use Arcgis software, click on the “elements of the folding point to point” function, the building footprint data into point data, and then converted to the csv format. csv format.  
  
  
项目介绍：根据地理空间坐标爬取百度街景(爬取当前坐标位置的所有百度街景数据)  
项目优点：可以爬取百度街景数据  
项目详情：本项目通过遍历地理空间坐标的方法，逐一搜索各坐标的百度街景历史数据与最新数据  
代码使用前提：  
1.自备地理空间坐标数据，数据需为csv(UTF-8)格式，同时使用地理坐标系；  
2.倘若你的数据不是csv(UTF-8)格式的，可以将你的数据转换为该格式，例如：将shp数据导为csv格式的数据，并使用记事本软件将其转换为csv(UTF-8)格式；  
3.为了进一步提高街景爬取的效率，用户可以按建筑物足迹数据进行提取，使用建筑物足迹数据（建筑物适量边界数据）的简单思路是：使用Arcgis软件，点击“要素折点转点”功能，将建筑物足迹数据转为点数据，再将其转为csv格式。
