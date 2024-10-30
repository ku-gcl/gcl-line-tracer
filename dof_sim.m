%% ライントレースのシミュレーション用コード
%% コードの流れ
% 画像からピクセルを読み取る
% センサの値から入力を決定する
% 状態方程式で運動を決定



%% スクリプトの初期化
close all;  %close all figures
clear;      %clear all variables
clc;        %clear the command terminal
format long
%warning off

% line width
set(0, 'DefaultLineLineWidth', 0.8) % default 0.5pt
set(0, 'DefaultAxesLineWidth', 0.8)
set(0, 'DefaultTextLineWidth', 0.8)

% font size
set(0, 'DefaultTextFontSize', 13)
set(0, 'DefaultAxesFontSize', 13)

% font name
set(0, 'DefaultTextFontName', 'Times New Roman')
set(0, 'DefaultAxesFontName', 'Times New Roman')
set(0, 'DefaultTextInterpreter', 'Latex')
set(0, 'DefaultLegendInterpreter', 'Latex')

% figure color
set(0, 'DefaultFigureWindowStyle', 'docked');
set(gcf, 'Color', 'none');
set(gca, 'Color', 'none');
set(gcf, 'InvertHardCopy', 'off');

close

myTimer = tic;        %start timer

%% 変数の一覧
%x,y: position [m]
%theta: angle [rad]
%v: velocity [m/s]
%omg: omega [rad/s]
%omg_R: right-handed omega [rad/s]
%omg_L: left-handed omega [rad/s]
%vR: right-handed velocity [m/s]
%vL: left-handed velocity [m/s]
%rwm: half of diameter [m]
%ttm: tred between two wheels [m]
%delt: delta t
rwm = 0.03;%[m]
ttm = 0.086;%[m]

%% 時間
delt = 20;
time_fin = 3000;
ts = 0:delt:time_fin;

%% 状態方程式の変数
Adof = eye(3);
Cdof = eye(3);
% Bは後で定義する

%% ロードマップを読み取る
h = figure();
hold on
him = imshow("figure/line.jpg");
I = imread("figure/line.jpg");
im = imagemodel(him);
display(im)

%% スタート地点
xref = 100;
yref = 1080;

%% PID 制御の変数の初期化
%初期条件
Xpid = zeros(3,length(ts));%x,y,and theta
Xpid(:,1) = [xref;yref;1];
Xpid_n = Xpid(:,1);
err = zeros(length(ts),1);
%PID制御のゲイン
% P ゲイン
Kp = 1;

%ストップ
count = 0;
%セルの初期化
px_Value_CELL = cell(length(ts)-1,1);

%回転行列
urot = [rwm/2,rwm/2;rwm/ttm,-rwm/ttm];

%センサーが読み取り可能な範囲--半径
theta = linspace(0,2*pi,360);
rc = 1e-2;%[m]

%平進運動のための角速度
omg_R_nom = 1;
omg_L_nom = 1;

%% PID 制御
for t=1:length(ts)-1
    %センサ1の中心
    cX1 = Xpid_n(1);%+ttm/2.*cos(Xpid_n(3));
    cY1 = Xpid_n(2)+ttm/2;

    %センサ2の中心
    cX2 = Xpid_n(1);%-ttm/2.*cos(Xpid_n(3));
    cY2 = Xpid_n(2)-ttm/2;

    % センサ1
    %ピクセル行列の値を格納
    pxValue_full = zeros(length(theta),3);
    for th=1:length(theta)
        cXth = cX1 + rc.*cos(theta(th));
        cYth = cY1 + rc.*sin(theta(th));
        %ピクセル局値を読み取り
        pxValue1 = getPixelValue(im,fix(cYth),fix(cXth));
        pxValue_full(th,:) = pxValue1;
    end
    %セルに格納
    px_Value_CELL{t,1} = pxValue_full;

    %ピクセル行列の平均をとる
    current_px = mean(pxValue_full);

    %ピクセル行列の平均から，黒(参照軌道)の差の割合
    %どのくらい白か？
    %black --[0,0,0]
    %white --[255,255,255]
    err(t) =  current_px(1)/255;

    %角速度ベクトルRの更新
    omg_R = err(t);

    % センサ2
    %ピクセル行列の値を格納
    pxValue_full = zeros(length(theta),3);
    for th=1:length(theta)
        cXth = cX2 + rc.*cos(theta(th));
        cYth = cY2 + rc.*sin(theta(th));
        %ピクセル局値を読み取り
        pxValue2 = getPixelValue(im,fix(cYth),fix(cXth));
        pxValue_full(th,:) = pxValue2;
    end
    %セルに格納
    px_Value_CELL{t,1} = pxValue_full;

    %ピクセル行列の平均をとる
    current_px = mean(pxValue_full);

    %ピクセル行列の平均から，黒(参照軌道)の差の割合
    %どのくらい白か？
    %black --[0,0,0]
    %white --[255,255,255]
    err(t) =  current_px(1)/255;

    %角速度ベクトルLの更新
    omg_L = err(t);

    %フィードバック入力
    u = urot*[omg_R_nom;omg_L_nom];
    up = Kp.*urot*[omg_R;omg_L];

    %状態方程式
    Bdof = [cos(Xpid_n(3))*delt,0;sin(Xpid_n(3))*delt,0;0,delt];
    Xpid_n = Adof*Xpid_n + Bdof*(u-up);
    Xpid(:,t+1) = Xpid_n;
end

%% 図をプロット
htx = figure();
hold on
grid on
box on
xlabel("$t$[s]");
ylabel("$x$[m]");
plot(ts,Xpid(1,:),'b','Linewidth',2);
hold off

hty = figure();
hold on
grid on
box on
xlabel("$t$[s]");
ylabel("$y$[m]");
plot(ts,Xpid(2,:),'b','Linewidth',2);
hold off

hxy = figure();
hold on
grid on
box on
xlabel("$x$[m]");
ylabel("$y$[m]");
xlim([min(Xpid(1,:)) max(Xpid(1,:))]);
ylim([980 1140]);
href = yline(Xpid(2,1),'-','reference');
href1 = yline(1050,'--','border');
href2 = yline(1100,'--','border');
hupid = plot(Xpid(1,:),Xpid(2,:),'b','Linewidth',2);
%linetrace
ppid = plot(Xpid(1,1),Xpid(2,1),'s','MarkerEdgeColor','r','MarkerSize',12);
v = VideoWriter("linetrace","MPEG-4");
open(v)
for frame = 1:length(Xpid(1,:))
    ppid.XData = Xpid(1,frame);
    ppid.YData = Xpid(2,frame);
fr = getframe(gcf);
%writeVideo(v,fr);
end
%legend([hu,hupid],{'reference','pid trajectory'},'Location','north');
hold off
close(v)



