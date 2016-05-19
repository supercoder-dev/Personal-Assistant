X1 = [51 5 4];
X2 = [41 10 9];

figure
ax1 = subplot(1,2,1);
labels = {'Correct evaluation','Correct evaluation with mistakes ','Incorrect evaluation'};
b = bar(ax1,[X1(1); 0; 0])
hold on 
b = bar(ax1,[0; X1(2); 0 ])
b(1).FaceColor = [0 .75 .75];

b = bar(ax1,[0; 0; X1(3) ])
b(1).FaceColor = 'yellow';
set(gca,'XTickLabel',{'','',''});
set(gca,'fontsize',20)
title(ax1,'Speech-to-text - without echo','FontSize', 22);

ax2 = subplot(1,2,2);
b = bar(ax2,[X2(1); 0; 0])
hold on 
b = bar(ax2,[0; X2(2); 0 ])
b(1).FaceColor = [0 .75 .75];
b = bar(ax2,[0; 0; X2(3) ])
b(1).FaceColor = 'yellow';

set(gca,'XTickLabel',{'','',''});
set(gca,'fontsize',20)
legend(labels, 'FontSize', 20);
title(ax2,'Speech-to-text - common enviroment','FontSize', 22);

%%

X1 = [30 10];
X2 = [30 3 1 6];

figure
ax1 = subplot(1,3,1);
labels = {'75%','25%'};
explode = [1 0];
pie(ax1,X1,explode,labels)
set(gca,'fontsize',24)
h=pie(ax1,X1,labels);
set(h(2:2:4),'FontSize',24);
title(ax1,'Complete system testing','FontSize', 28);
legend({'Correct evaluation','Incorrect evaluation'}, 'FontSize', 24);

labels = {'Successfull query','Attention word faliure', 'Speech-to-text faliure', 'Sentence processing faliure'};
ax2 = subplot(1,2,2);
b = bar(ax2,[X2(1); 0; 0;0])
hold on 
b = bar(ax2,[0; X2(2); 0 ;0])
b(1).FaceColor = [0 .75 .75];
b = bar(ax2,[0; 0; X2(3) ;0])
b(1).FaceColor = 'yellow';
b = bar(ax2,[0; 0;0; X2(4) ])
b(1).FaceColor = [0.6 .2 0];
set(gca,'XTickLabel',{'','',''});
set(gca,'fontsize',24)
legend(labels, 'FontSize', 24);
title(ax2,'Specific modul faliures','FontSize', 28);