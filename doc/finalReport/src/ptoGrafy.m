%% testovani klicoveho slova 
figure
confusion_matrix = [25 16 9 NaN;
                    25 25 0 NaN;
                    25 24 1 NaN;
                    25 21 4 NaN;
                    25 21 4 NaN];
%bar chart
bar3(confusion_matrix(:,[4,2]), 'g');
hold on
bar3(confusion_matrix(:,[3,4]), 'r');
 

% x vals are the columns of confusion, ys are the rows of confusion
set(gca,'XTickLabel',{'Nagative', 'Positive', 'Number of tests' });
set(gca,'YTickLabel',{'Jakub Drapela', 'Martin Klucka - Set 1', 'Jakub Konrad - Set 1','Martin Klucka - Set 2','Jakub Konrad - Set 2'});
% ylabel('Testujici soba');
zlabel('Number of detections');
title('Test Attention word  - calm room')
%% Test celeho systemu 

%Attention word
TP = 32; FP = 8; FN = 4;
X1 = [TP,FP,FN];
%Speech recognition
TP = 22; FP = 4; FN = 6;
X2 = [TP,FP,FN];
%Answers
T = 23; F= 3;
X3 = [T,F];


figure
ax1 = subplot(1,3,1);
labels = {'TP','FP','FN'};
explode = [1 0 0];
pie(ax1,X1,explode,labels)
title(ax1,'Attention word');

ax2 = subplot(1,3,2);
labels = {'True','True (s chybami)','False'};
explode = [1 1 0];
pie(ax2,X2,explode,labels)
title(ax2,'Speech recognition');

ax2 = subplot(1,3,3);
labels = {'True', 'False'};
explode = [1 0];
pie(ax2,X3,explode,labels)
title(ax2,'Answers');

%%

%Sentence processing
TP = 40; FP = 8;
X1 = [TP,FP];

TP = 22; FP = 1;
X2 = [TP,FP];

T = 18; F= 7;
X3 = [T,F];


figure
ax1 = subplot(1,3,1);
labels = {'Správnì vyhodnoceno','Incorrect evaluation'};
explode = [1 0];
pie(ax1,X1,explode,labels)
title(ax1,'Sentence processing');

ax2 = subplot(1,3,2);
labels = {'Správnì vyhodnoceno','Incorrect evaluation'};
explode = [1 0];
pie(ax2,X2,explode,labels)
title(ax2,'Sentence processing - valid queries');

ax3 = subplot(1,3,3);
labels = {'Správnì vyhodnoceno','Incorrect evaluation'};
explode = [1 0];
pie(ax3,X3,explode,labels)
title(ax3,'Sentence processing - out of scope queries');


%%
X1 = [0 0 0];
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

