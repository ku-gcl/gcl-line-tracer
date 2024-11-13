import time
import sys
import os

# 現在のスクリプトの位置から親ディレクトリを取得して追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from NatNetSDK.NatNetClient import NatNetClient

client = NatNetClient()




