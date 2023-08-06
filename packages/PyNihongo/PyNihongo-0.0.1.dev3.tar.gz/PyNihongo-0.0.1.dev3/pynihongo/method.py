"""
@Project: https://github.com/KouShoken/pynihongo
@Time: 西暦2023年6月16日 22:00
@Author: KouShoken

This is an open source project that uses the MIT protocol. 
While I don't make any demands, But　I think respecting copyright 
maybe is a basic morality.
"""


class Method:

    @staticmethod
    def to_seion(text: str) -> str:
        trans = str.maketrans({
            'が': 'か', 'ぎ': 'き', 'ぐ': 'く', 'げ': 'け', 'ご': 'こ',
            'ざ': 'さ', 'じ': 'し', 'ず': 'す', 'ぜ': 'せ', 'ぞ': 'そ',
            'だ': 'た', 'ぢ': 'ち', 'づ': 'つ', 'で': 'て', 'ど': 'と',
            'ば': 'は', 'び': 'ひ', 'ぶ': 'ふ', 'べ': 'へ', 'ぼ': 'ほ',
            'ぱ': 'は', 'ぴ': 'ひ', 'ぷ': 'ふ', 'ぺ': 'へ', 'ぽ': 'ほ',
        })
        return text.translate(trans)


class JapanCountries:
    @staticmethod
    def all():
        """
        With Hokkaito Chiho
        :return:
        """

        return [
            {
                "name": "北海道",
                "countries": ['北海道']
            },
            {
                "name": "東北",
                "countries": ['青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県']
            },
            {
                "name": "関東",
                "countries": ['茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県']
            },
            {
                "name": "中部",
                "countries": ['新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県']
            },
            {
                "name": "近畿",
                "countries": ['三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県']
            },
            {
                "name": "中国",
                "countries": ['鳥取県', '島根県', '岡山県', '広島県', '山口県']
            },
            {
                "name": "四国",
                "countries": ['徳島県', '香川県', '愛媛県', '高知県']
            },
            {
                "name": "九州",
                "countries": ['福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']
            },
        ]

    @staticmethod
    def with_no_hokkaitoChiho():
        """
        With No Hokkaito Chiho
        :return:
        """
        chiho_list = JapanCountries.all()
        chiho_list[1]["name"] = "北海道・東北"
        chiho_list[1]["countries"] = chiho_list[0]["countries"] + chiho_list[1]["countries"]
        del chiho_list[0]
        return chiho_list
