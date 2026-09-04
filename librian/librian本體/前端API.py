class 山彥API:
    """Librian 前端可調用的後端 API。"""

    def __init__(self, 山彥):
        self._山彥 = 山彥

    def vue更新(self, 內容):
        return self._山彥.vue更新(內容)

    def 取檔(self):
        return self._山彥.取檔()

    def 存檔(self, 文件名, 描述, 截圖):
        return self._山彥.存檔(文件名, 描述, 截圖)

    def 讀檔(self, 文件名):
        return self._山彥.讀檔(文件名)

    def 快速存檔(self):
        return self._山彥.快速存檔()

    def 快速讀檔(self):
        return self._山彥.快速讀檔()

    def 切換全屏(self):
        return self._山彥.切換全屏()

    def 回標題(self):
        return self._山彥.回標題()

    def 步進(self):
        return self._山彥.步進()

    def 更新(self, 瞬間化=False):
        return self._山彥.更新(瞬間化)

    def 狀態回調(self, 步進):
        return self._山彥.狀態回調(步進)

    def 初始化(self):
        return self._山彥.初始化()

    def 選(self, 參數):
        return self._山彥.選(參數)

    def 開始(self):
        return self._山彥.開始()

    def 讀檔畫面(self):
        return self._山彥.讀檔畫面()

    def 從劇本開始(self, 劇本):
        return self._山彥.從劇本開始(劇本)

    def 更新終態(self):
        return self._山彥.更新終態()
