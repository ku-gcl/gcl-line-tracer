from NatNetClient import NatNetClient
import time
import sys

# NatNetサーバー（OptiTrack）のIPアドレス
SERVER_IP = "192.168.1.196"  # 実際のサーバーIPに置き換えてください

# クライアントのIPアドレス（必要に応じて設定）
CLIENT_IP = "192.168.1.65"    # 自分のマシンのIPアドレスに置き換えてください

# クライアントのインスタンスを作成
client = NatNetClient()

# サーバーおよびクライアントのIPアドレスを設定
client.set_server_address(SERVER_IP)
client.set_client_address(CLIENT_IP)  # 必要に応じて設定。指定しない場合はデフォルト

# マルチキャストアドレスを使用する場合は以下を設定
client.set_use_multicast(True)  # マルチキャストを使用しない場合はFalseに設定

# データ受信時のコールバック関数を定義
def receive_frame(data):
    print("フレームデータを受信:")
    print(f"フレーム番号: {data.get('frame_number')}")
    print(f"リジッドボディ数: {data.get('rigid_body_count')}")
    print(f"スケルトン数: {data.get('skeleton_count')}")
    print(f"アセット数: {data.get('asset_count')}")
    print(f"ラベル付きマーカー数: {data.get('labeled_marker_count')}")
    print(f"タイムコード: {data.get('timecode')}")
    print(f"タイムコードサブ: {data.get('timecode_sub')}")
    print(f"タイムスタンプ: {data.get('timestamp')}")
    print(f"録画中: {data.get('is_recording')}")
    print(f"トラッキングモデル変更: {data.get('tracked_models_changed')}")
    print("-" * 50)

    # ここでさらにリジッドボディの詳細情報を取得する場合は、
    # MoCapData クラスや他のデータ構造を拡張する必要があります。
    # 現在のNatNetClient.pyの実装では、詳細なリジッドボディ情報はdata_dictに含まれていません。
    # 必要に応じて、NatNetClient.pyを修正して詳細データをコールバックに渡すようにしてください。

# コールバック関数を登録
client.new_frame_listener = receive_frame

try:
    # クライアントを実行（接続）
    if client.run():
        print(f"NatNetサーバー（{SERVER_IP}）に接続しました。データ受信を開始します。Ctrl+Cで停止します。")
    else:
        print("クライアントの実行に失敗しました。")
        sys.exit(1)

    # データ受信を維持するためのループ
    while True:
        time.sleep(1)  # メインスレッドを維持

except KeyboardInterrupt:
    print("\nプログラムを終了します。")

finally:
    # クライアントをシャットダウン（切断）
    client.shutdown()
    print("NatNetクライアントを切断しました。")
