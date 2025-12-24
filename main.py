import sys
from Api.Register import Register
from Api.Sales import Sales
from Api.State import State
from Api.Stock import Stock
from Api.Auth import Auth
from Models.Base import Base
from Models.UserModel import UserRole
from Services.AuthService import AuthService
from Services.RefundService import RefundService
from Services.RegisterService import RegisterService
from Services.ReportService import ReportService
from Services.StockService import StockService
from Repositories.ProductRepository import ProductRepository
from Repositories.RefundRepository import RefundRepository
from Repositories.SaleItemRepository import SaleItemRepository
from Repositories.SaleRepository import SaleRepository
from Repositories.UserRepository import UserRepository
import webview
import os
from Utilities.Database import engine


class API:
    def __init__(self):
        self.product_repo = ProductRepository()
        self.refund_repo = RefundRepository()
        self.sale_item_repo = SaleItemRepository()
        self.sale_repo = SaleRepository()
        self.user_repo = UserRepository()

        self.auth_service = AuthService(self.user_repo)
        self.refund_service = RefundService(self.product_repo, self.sale_repo, self.sale_item_repo, self.refund_repo)
        self.register_service = RegisterService(self.product_repo, self.auth_service)
        self.report_service = ReportService(self.sale_item_repo, self.sale_repo, self.product_repo)
        self.stock_service = StockService(self.product_repo, self.sale_item_repo)

        self.stock = Stock(self.stock_service)
        self.auth = Auth(self.auth_service)
        self.register = Register(self.auth_service, self.register_service)
        self.state = State(self.auth_service)
        self.sales = Sales(self.report_service, self.refund_service)
    
    def debug(self, message):
        print(message)
        
    def close_app(self):
        sys.exit(0)


def main():

    api = API()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "UI", "web", "splash.html")
    if api.auth_service.count_users() == 0:
        api.auth.add_user("admin", "admin", UserRole.ADMIN)

    webview.create_window("Store Manager", html_path, js_api=api, fullscreen=True,)
    webview.start()

if __name__ == "__main__":
    main()
