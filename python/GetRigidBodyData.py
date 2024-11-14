import time
from NatNetSDK.NatNetClient import NatNetClient

# 「RigidBody1」のデータを取得するためのコールバック関数
def receive_rigid_body_frame(new_id, position, rotation):
    # if new_id == "drone":  # IDが「RigidBody1」と一致するかを確認
    print("drone Data:")
    print(f"Position (x, y, z): {position}")
    print(f"Rotation (qw, qx, qy, qz): {rotation}")

def main():
    # NatNetClientの設定
    client = NatNetClient()
    client.rigid_body_listener = receive_rigid_body_frame  # コールバックを設定

    # クライアントの接続設定（必要に応じてIPアドレスを変更してください）
    client.set_client_address("192.168.1.65")  # クライアントのIPアドレスを設定
    client.set_server_address("192.168.1.196")  # サーバー（モーションキャプチャデータ送信元）のIPアドレスを設定
    client.set_use_multicast(True)  # 必要に応じてマルチキャストを使用

    # ストリーミングクライアントを開始
    if not client.run():
        print("ERROR: Could not start streaming client.")
        return

    print("Waiting for data... Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)  # データ待機
    except KeyboardInterrupt:
        print("\nStopping client...")
        client.shutdown()

if __name__ == "__main__":
    main()
