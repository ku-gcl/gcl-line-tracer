% パラメータ設定
dt = 0.1; % タイムステップ
T = 20; % シミュレーション時間
time = 0:dt:T; % 時間ベクトル

% ラインの定義（直線）
line_x = linspace(0, 10, 100);
line_y = 5 + 2*sin(line_x); % サイン波のライン

% ライントレーサーの初期位置
robot_x = 0;
robot_y = 5; % 初期y座標
theta = 0; % 初期角度
v = 0.2; % 直進速度
omega = 0; % 初期角速度

% シミュレーションの実行
figure;
hold on;
plot(line_x, line_y, 'k', 'LineWidth', 2); % ラインをプロット
robot_plot = plot(robot_x, robot_y, 'ro', 'MarkerSize', 10); % ロボットの位置

for t = time
    % ラインとの距離を計算
    error = interp1(line_x, line_y, robot_x) - robot_y; % y方向の誤差

    % 制御入力の計算（比例制御）
    omega = error * 0.5; % 角速度を誤差に基づいて更新
    
    % ダイナミクスの更新
    robot_x = robot_x + v * cos(theta) * dt; % x座標の更新
    robot_y = robot_y + v * sin(theta) * dt; % y座標の更新
    theta = theta + omega * dt; % 角度の更新

    % プロットの更新
    set(robot_plot, 'XData', robot_x, 'YData', robot_y);
    pause(dt);
end

hold off;