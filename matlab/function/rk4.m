% ルンゲ・クッタ法の定義
function y = rk4(func, t, h, y, varargin)
    k1 = h * func(t, y, varargin{:});
    k2 = h * func(t + 0.5 * h, y + 0.5 * k1, varargin{:});
    k3 = h * func(t + 0.5 * h, y + 0.5 * k2, varargin{:});
    k4 = h * func(t + h, y + k3, varargin{:});
    y = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6;
end