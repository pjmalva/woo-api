import pymssql

# SELECT CE.ESTRUTURA 'CATEGORY_CODE',
#     CE.DESCRICAO 'CATEGORY_NAME'
# FROM CADEST CE
# WHERE CE.ESTRUTURA NOT IN ('20.01.01')
# ORDER BY CE.DESCRICAO

class StarTwo:
    def __init__(self, host, user, passwd, database):
        self.conn = pymssql.connect(host, user, passwd, database)

    def makeSelect(self, sql):
        cursor = self.conn.cursor()
        registers = cursor.execute(sql)
        self.conn.close()
        return registers

    def updateCategories(self):
        sql = """
            SELECT CE.ESTRUTURA 'CATEGORY_CODE',
                CE.DESCRICAO 'CATEGORY_NAME'
            FROM CADEST CE
            WHERE CE.ESTRUTURA NOT IN ('20.01.01')
            ORDER BY CE.DESCRICAO
        """

        self.registros = []
        for registro in self.makeSelect(sql):
            self.registros.append(
                {
                    'code': registro[0],
                    'name': registro[1],
                }
            )
        return self.registros


    def updateProducts(self, minimunStock=1):
        sql = """
            SELECT CD.MERCADORIA, CD.NOME_M, CD.UR, CS.PRECO,
                CS.PROMOCAO, CS.INI_PROM, CS.VAL_PROM,
                dbo.calculaEstoque(
                    CD.MERCADORIA, '1', convert(date, getdate())
                ) as 'ESTOQUE',
                CE.ESTRUTURA 'CATEGORY_CODE',
                CE.DESCRICAO 'CATEGORY_NAME'
            FROM CADMER CD
            LEFT OUTER JOIN CUSTOS CS
            ON CS.MERCADORIA = CD.MERCADORIA
            INNER JOIN CADEST CE
            on CE.ESTRUTURA = CD.ESTRUTURA
            WHERE CS.PRECO > 0
            AND CD.TIPO_ITEM = '00'
            AND CD.CONTROLE <>'B'
            AND CD.ESTRUTURA NOT IN ('20.01.01')
            GROUP BY CD.MERCADORIA, CD.NOME_M, CD.UR, CS.PRECO,
            CS.PROMOCAO, CS.INI_PROM, CS.VAL_PROM,CE.ESTRUTURA, CE.DESCRICAO
            ORDER BY CD.NOME_M
        """

        self.registros = []
        for registro in self.makeSelect(sql):
            if float(registro[7]) >= minimunStock:
                self.registros.append(
                    {
                        'reference': registro[0],
                        'name': registro[1],
                        'unity': registro[2],
                        'price': registro[3],
                        'price_sale': registro[4],
                        'sale_start': registro[5],
                        'sale_finish': registro[6],
                        'stock': registro[7],
                        'category_code': registro[8],
                        'category_name': registro[9],
                    }
                )
        return self.registros
