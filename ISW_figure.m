clear;clc
load('mycmap.mat')
%%
% sulu  Sea
lon_lim=[117 120];
lat_lim=[6.5 9];
[topo, refvec] = etopo('etopo1_bed_c_f4.flt', 1, lat_lim, lon_lim);
lon=linspace(lon_lim(1,1),lon_lim(1,2),size(topo,2));
lat=linspace(lat_lim(1,1),lat_lim(1,2),size(topo,1));
sulu.lon=lon;
sulu.lat=lat;
sulu.topo=topo;
sulu.topo(sulu.topo>=0)=nan;

%%
figure
clf
set(gcf,'position',[800 100 800 600]);%设置了figure的位置：起始坐标为10,60，这是显示器的像素值。图宽度为900个像素，高度为700像素。
m_proj('Equidistant Cylindrical','lon',[lon_lim(1),lon_lim(end)],'lat',[lat_lim(1),lat_lim(end)]);
hold on
m_gshhs_i('patch',[.6 .6 .6]);%岸线
m_proj('Equidistant Cylindrical', 'lon', [lon_lim(1), lon_lim(end)], 'lat', [lat_lim(1), lat_lim(end)], 'rectbox', 'on');
m_contourf(sulu.lon,sulu.lat,sulu.topo,50,'linestyle','none')
m_grid('linest','none','tickdir','out','box','fancy','fontsize',18);
colormap(mycmap.topo);
caxis([-5000 0])
set(gcf,'color','w');
hold on;

% c=colorbar('position',[.768 .63 .035 .18]);set(c,'ticklength',0.14);
c=colorbar('eastoutside');
set(c,'ytick',[-5000:1000:0],'yticklabel',[-5000:1000:0],'fontsize',14,'fontweight','bold','xaxislocation','right')

%画框
% m_plot([119.5,119.5],[5.5,6.5],'color','r','linewidth',1.5);
% m_plot([120.5 120.5],[5.5 6.5],'color','r','linewidth',1.5);
% m_plot([119.5 120.5],[5.5 5.5],'color','r','linewidth',1.5);
% m_plot([119.5 120.5],[6.5 6.5],'color','r','linewidth',1.5);

%% 

%加上波峰线
filename=dir('D:\Desktop\内波信息提取\2024.8.1观测结果\苏禄海-2024.8.4\内波提取\csv\*.csv');
hold on
LON=[];LAT=[];
for i=1:1:length(filename)
    if filename(i).bytes<=0
        disp(i)
    clear lon lat lon_lat Lon Lat
    else
lon_lat=load(['D:\Desktop\内波信息提取\2024.8.4观测结果\苏禄海-2024.8.4\内波提取\csv\',filename(i).name]);
lon=lon_lat(:,1);
lat=lon_lat(:,2);
%[Lon,Lat]=filter_crest(lon,lat);
%if length(Lon)>10000
m_plot(lon,lat,'or','markersize',0.4)
%end
    end
end
% save('G:\2022研究生课程讲义及课件\论文所需文献资料\绘图csv文件\results\crest.mat','LON','LAT')
% print(gcf,'G:\2022研究生课程讲义及课件\论文所需文献资料\绘图csv文件\results\southchinasea_crest.png','-dpng','-r600')
drawnow;
%% 

%加上波峰线
filename=dir('D:\Desktop\内波信息提取\2024.8.20观测结果\苏禄海-2024.8.20\内波提取\csv\*.csv');
hold on
LON=[];LAT=[];
for i=1:1:length(filename)
    if filename(i).bytes<=0
        disp(i)
    clear lon lat lon_lat Lon Lat
    else
lon_lat=load(['D:\Desktop\内波信息提取\2024.8.20观测结果\苏禄海-2024.8.20\内波提取\csv\',filename(i).name]);
lon=lon_lat(:,1);
lat=lon_lat(:,2);
%[Lon,Lat]=filter_crest(lon,lat);
%if length(Lon)>10000
m_plot(lon,lat,'ok','markersize',0.4)
%end
disp(i)
clear lon lat lon_lat Lon Lat
    end
end
% save('G:\2022研究生课程讲义及课件\论文所需文献资料\绘图csv文件\results\crest.mat','LON','LAT')
% print(gcf,'G:\2022研究生课程讲义及课件\论文所需文献资料\绘图csv文件\results\southchinasea_crest.png','-dpng','-r600')
%% 标注地名
% gtext('苏禄海','fontsize',16,'fontweight','bold','fontsmoothing','on','color','k');
% gtext('苏拉威西海','fontsize',11,'fontweight','bold','fontsmoothing','on','color','k');
% %str={'太','平','洋'};
%gtext(str,'fontsize',11,'fontweight','bold','fontsmoothing','on','color','k');
% gtext('南海','fontsize',13,'fontweight','bold','fontsmoothing','on','color','k');

% gtext('菲律宾群岛','fontsize',13,'fontweight','bold','fontsmoothing','on','color','k');
% gtext('台湾岛','fontsize',13,'fontweight','bold','fontsmoothing','on','color','k');
% gtext('中华人民共和国','fontsize',13,'fontweight','bold','fontsmoothing','on','color','k');

% gtext('太平洋','fontsize',13,'fontweight','bold','fontsmoothing','on','color','k');
% gtext('巴','fontsize',16,'fontweight','bold','fontsmoothing','on','color','k');
% gtext('拉','fontsize',16,'fontweight','bold','fontsmoothing','on','color','k');
% gtext('望','fontsize',16,'fontweight','bold','fontsmoothing','on','color','k');
% gtext('岛','fontsize',16,'fontweight','bold','fontsmoothing','on','color','k');
% 
% print(gcf,'G:\2022研究生课程讲义及课件\论文所需文献资料\绘图csv文件\results','-dpng','-r600')

% print(gcf,'G:\2022研究生课程讲义及课件\论文所需文献资料\绘图csv文件\results\southchinasea_crest_fliter.png','-dpng','-r600')


