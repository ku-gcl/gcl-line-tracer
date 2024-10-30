% https://rikei-tawamure.com/entry/2020/07/24/162236
%

% ランタイムの設定
clc;
clear;
close all;

% ルンゲ・クッタ法の定義
function y = rk4(func, t, h, y, varargin)
    k1 = h * func(t, y, varargin{:});
    k2 = h * func(t + 0.5 * h, y + 0.5 * k1, varargin{:});
    k3 = h * func(t + 0.5 * h, y + 0.5 * k2, varargin{:});
    k4 = h * func(t + h, y + k3, varargin{:});
    y = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6;
end

% ロボットの仕様
function [V, xms, yms] = robot_spec()
    V = 3; % ロボット速度[m/s]
    xms = 0.15; % センサ位置x[m]
    yms = 0.0; % センサ位置y[m]
end

% 導関数の定義
function out = omegadot(t, omega, omegaref)
    tau = 0.035;
    out = -omega / tau + omegaref / tau;
end

function out = psidot(t, psi, omega)
    out = omega;
end

function out = xmdot(t, xm, psi)
    [V, xms, yms] = robot_spec();
    out = V * cos(psi);
end

function out = ymdot(t, ym, psi)
    [V, xms, yms] = robot_spec();
    out = V * sin(psi);
end

function out = _xs(xm, ym, xms, yms, psi)
    out = cos(psi) * xms - sin(psi) * yms + xm;
end

function out = _ys(xm, ym, xms, yms, psi)
    out = sin(psi) * xms + cos(psi) * yms + ym;
end

% ログ変数の初期化
Xs = [];
Ys = [];
Xm = [];
Ym = [];
Psi = [];
Psi_dot = [];
Psi_dot_com = [];
Minls = [];
T = [];

% ゲイン設定
[V, xms, yms] = robot_spec();
Kp = 1250;
Kd = 0;

% コース
r1 = 1;
x10 = 0; y10 = 0;
x20 = -2.5; y20 = -1e5;
x30 = -5; y30 = 0;
x40 = -2.5; y40 = 1e5;
r2 = sqrt((x20 - 0)^2 + (y20 - r1)^2);
r3 = r1;
r4 = r2;

% 状態変数等の初期化
t = 0.0;
xm = 0;
ym = r1;
psi = pi;
omega = 0;
yref = 1.0;
xs = _xs(xm, ym, xms, yms, psi);
ys = _ys(xm, ym, xms, yms, psi);

% センサがあるエリアで場合分け
if xs >= 0
    s1 = sqrt((xs - x10)^2 + (ys - y10)^2);
    ls1 = s1 - r1;
    minls = ls1;
elseif xs <= -5.0
    s3 = sqrt((xs - x30)^2 + (ys - y30)^2);
    ls3 = s3 - r1;
    minls = ls3;  
elseif ys > 0
    s2 = sqrt((xs - x20)^2 + (ys - y20)^2);
    ls2 = s2 - r2;
    minls = ls2;
else
    s4 = sqrt((xs - x40)^2 + (ys - y40)^2);
    ls4 = s4 - r2;
    minls = ls4;
end

psi_dot_com = Kp * minls;
oldminls = minls;

% 刻み幅
h = 1e-5;

% 制御周期
Cpriod = 1e-3;
_Cpriod = Cpriod / h;

% 計算時間(s)
TrackLength = 16; % [m]
Tcalc = TrackLength / V;
N = round(Tcalc / h);

% メインループ
for n = 1:N
    Xm(end + 1) = xm;
    Ym(end + 1) = ym;
    Xs(end + 1) = xs;
    Ys(end + 1) = ys;
    Psi(end + 1) = psi * 180 / pi;
    Psi_dot(end + 1) = omega * 180 / pi;
    Psi_dot_com(end + 1) = psi_dot_com * 180 / pi;
    Minls(end + 1) = minls;
    T(end + 1) = t;

    % ライン検知
    if mod(n, _Cpriod) == 0
        % センサがあるエリアで場合分け
        if xs >= 0
            s1 = sqrt((xs - x10)^2 + (ys - y10)^2);
            ls1 = s1 - r1;
            minls = ls1;
        elseif xs <= -5.0
            s3 = sqrt((xs - x30)^2 + (ys - y30)^2);
            ls3 = s3 - r1;
            minls = ls3;
        elseif ys > 0
            s2 = sqrt((xs - x20)^2 + (ys - y20)^2);
            ls2 = s2 - r2;
            minls = ls2;
        else
            s4 = sqrt((xs - x40)^2 + (ys - y40)^2);
            ls4 = s4 - r2;
            minls = ls4;
        end

        % 制御
        psi_dot_com = Kp * minls + Kd * (minls - oldminls) / Cpriod;
    end
    
    % 状態変数保存    
    oldminls = minls;
    oldpsi = psi;
    oldys = ys;
    oldym = ym;
    oldxm = xm;
    oldomega = omega;
    
    % ルンゲ・クッタ呼び出し
    xm = rk4(@xmdot, t, h, oldxm, oldpsi);
    ym = rk4(@ymdot, t, h, oldym, oldpsi);
    omega = rk4(@omegadot, t, h, oldomega, psi_dot_com);
    psi = rk4(@psidot, t, h, oldpsi, oldomega);

    % センサ位置算出
    xs = _xs(xm, ym, xms, yms, psi);
    ys = _ys(xm, ym, xms, yms, psi);
    
    % 時間更新
    t = t + h;
end

% 最後の値を追加
Xm(end + 1) = xm;
Ym(end + 1) = ym;
Xs(end + 1) = xs;
Ys(end + 1) = ys;
Psi(end + 1) = psi * 180 / pi;
Psi_dot(end + 1) = omega * 180 / pi;
Psi_dot_com(end + 1) = psi_dot_com * 180 / pi;
Minls(end + 1) = minls;
T(end + 1) = t;

% グラフの描画
figure('Position', [100, 100, 1100, 1600]);

% ysのグラフ
subplot(5, 1, 1);
plot(T(1:10:end), Ys(1:10:end));
ylabel('ys[m]');
grid on;

% 角度のグラフ
subplot(5, 1, 2);
plot(T(1:10:end), Psi(1:10:end));
ylabel('Psi[deg]');
grid on;

% 角速度のグラフ
subplot(5, 1, 3);
plot(T(1:10:end), Psi_dot(1:10:end), 'DisplayName', 'Psi_dot');
hold on;
plot(T(1:10:end), Psi_dot_com(1:10:end), 'DisplayName', 'Command');
xlabel('Time[s]');
ylabel('PsiDot[deg/s]');
legend('Location', 'northwest');
grid on;

% 誤差のグラフ
subplot(5, 1, 4);
plot(T(1:10:end), Minls(1:10:end));
xlabel('Time[s]');
ylabel('Error[m]');
grid on;

% 走行軌跡のグラフ
subplot(5, 1, 5);
th1 = linspace(-pi/2, pi/2, 100000);
x1 = r1 * cos(th1);
y1 = r1 * sin(th1);
x20 = -2