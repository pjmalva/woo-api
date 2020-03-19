import pymssql

# SELECT CD.MERCADORIA, CD.NOME_M, CD.UR, CS.PRECO,
# 	   CS.PROMOCAO, CS.INI_PROM, CS.VAL_PROM,
# 	   dbo.calculaEstoque(CD.MERCADORIA, '1', convert(date, getdate())) as 'ESTOQUE'
#   FROM CADMER CD
#   LEFT OUTER JOIN CUSTOS CS
#     ON CS.MERCADORIA = CD.MERCADORIA
#  WHERE CS.PRECO > 0
#  GROUP BY CD.MERCADORIA, CD.NOME_M, CD.UR, CS.PRECO,
# 		CS.PROMOCAO, CS.INI_PROM, CS.VAL_PROM
#  ORDER BY CD.NOME_M

class StarTwo:
    def __init__(self, host, user, passwd, database):
        self.conn = pymssql.connect(host, user, passwd, database)

    def updateProducts(self):
        cursor = self.conn.cursor()

        sql = """
            SELECT CD.MERCADORIA, CD.NOME_M, CD.UR, CS.PRECO,
                CS.PROMOCAO, CS.INI_PROM, CS.VAL_PROM,
                dbo.calculaEstoque(
                    CD.MERCADORIA, '1', convert(date, getdate())
                ) as 'ESTOQUE'
            FROM CADMER CD
            LEFT OUTER JOIN CUSTOS CS
            ON CS.MERCADORIA = CD.MERCADORIA
            WHERE CS.PRECO > 0
            GROUP BY CD.MERCADORIA, CD.NOME_M, CD.UR, CS.PRECO,
            CS.PROMOCAO, CS.INI_PROM, CS.VAL_PROM
            ORDER BY CD.NOME_M
        """

        cursor.execute(sql)

        self.registros = []

        for registro in cursor:
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
                }
            )

        self.conn.close()

        return self.registros
