from flask import Flask, request, jsonify
from daos.account_dao_postgres import AccountDaoPostgres
from daos.client_dao_postgres import ClientDaoPostgres
from entities.account import Account
from entities.client import Client
from exceptions.account_not_found import AccountNotFoundError
from exceptions.client_not_found import ClientNotFoundError
from services.account_service_impl import AccountServiceImpl
from services.client_service_impl import ClientServiceImpl

acct_dao = AccountDaoPostgres()
client_dao = ClientDaoPostgres()
acct_service = AccountServiceImpl(acct_dao)
client_service = ClientServiceImpl(client_dao)


def create_routes(app: Flask):
    @app.post('/clients')
    def create_client():
        client = Client.json_deserialize(request.json)
        client_service.create_client(client)
        app.logger.info(f'New client registered ID: {client.client_id}')
        return jsonify(client.json()), 201

    @app.get('/clients')
    def get_all_clients():
        name = request.args.get('name')
        if name is None:
            clients = client_service.get_all_clients()
            dict_list = [client.json() for client in clients]
            return jsonify(dict_list), 200
        else:
            clients = client_service.get_client_by_name(name)
            dict_list = [client.json() for client in clients]
            if len(dict_list) == 0:
                return f"There are no clients with a name containing: {name}", 404
            return jsonify(dict_list), 200

    @app.get('/clients/<client_id>')
    def get_client_by_id(client_id: str):
        try:
            c = client_service.get_client(int(client_id))
            return jsonify(c.json()), 200
        except ClientNotFoundError as e:
            return e.message, 404

    @app.put('/clients/<client_id>')
    def update_client(client_id: str):
        try:
            client = Client.json_deserialize(request.json)
            client.client_id = int(client_id)
            client_service.update_client(client)
            return jsonify(client.json()), 200
        except ClientNotFoundError as e:
            return e.message, 404

    @app.delete('/clients/<client_id>')
    def remove_client(client_id: str):
        try:
            client_service.remove_client(int(client_id))
            app.logger.info(f'Deleted client ID: {client_id}')
            return 'Client deleted.', 205
        except ClientNotFoundError as e:
            return e.message, 404

    @app.post('/clients/<client_id>/accounts')
    def create_account(client_id: str):
        account = Account.json_deserialize(request.json)
        acct_service.create_acct(account, int(client_id))
        app.logger.info(f'New account registered ID: {account.acct_id}')
        return jsonify(account.json()), 201

    @app.get('/clients/<client_id>/accounts')
    def get_accounts_by_id(client_id: str):
        amount_less_than = request.args.get('amountLessThan')
        amount_greater_than = request.args.get('amountGreaterThan')
        if amount_less_than is None or amount_greater_than is None:
            accounts = acct_service.get_accounts_by_client_id(int(client_id))
            if len(accounts) == 0:
                return "Client does not exists", 404
            dict_list = [account.json() for account in accounts]
            return jsonify(dict_list), 200
        else:
            accounts = acct_service.get_accounts_in_range(int(client_id), float(amount_greater_than),
                                                          float(amount_less_than))
            dict_list = [account.json() for account in accounts]
            if len(dict_list) == 0:
                return "Client des not exists", 404
            return jsonify(dict_list), 200

    @app.get('/clients/<client_id>/accounts/<acct_id>')
    def get_account(client_id: str, acct_id: str):
        try:
            account = acct_service.get_acct_by_acct_id(int(acct_id))
            if account.client_id == int(client_id):
                return jsonify(account.json()), 200
            else:
                return "Client does not exists", 404
        except AccountNotFoundError as e:
            return e.message, 404
        except AttributeError:
            return "Account does not exist", 404

    @app.put('/clients/<client_id>/accounts/<acct_id>')
    def update_account(client_id: str, acct_id: str):
        try:
            acct_service.get_accounts_by_client_id(int(client_id))  # catches errors
            acct_service.get_acct_by_acct_id(int(acct_id))  # catches errors

            account = Account.json_deserialize(request.json)
            account.client_id = int(client_id)
            account.acct_id = acct_id
            acct_service.update_account(account)
            return jsonify(account.json()), 200
        except AccountNotFoundError as e:
            return e.message, 404
        except ClientNotFoundError as e:
            return e.message, 404

    @app.delete('/clients/<client_id>/accounts/<acct_id>')
    def remove_account(client_id: str, acct_id: str):
        try:
            if acct_service.get_acct_by_acct_id(int(acct_id)).client_id == int(client_id):
                acct_service.close_acct(int(acct_id))
                app.logger.info(f'Deleted account ID: {acct_id}')
                return "Account successfully deleted.", 205
            else:
                return "Account does not exist for that client.", 404
        except AccountNotFoundError as e:
            return e.message, 404
        except AttributeError:
            return "Client/Account not found.\nPlease enter valid information.", 404

    @app.patch('/clients/<client_id>/accounts/<acct_id>')
    def change_balance(client_id: str, acct_id: str):
        deposit = request.args.get('deposit')
        withdraw = request.args.get('withdraw')
        try:
            if acct_service.get_acct_by_acct_id(int(acct_id)).client_id != int(client_id):
                return "Account does not exist for that client.", 404
            if withdraw is not None:
                if acct_service.get_acct_by_acct_id(int(acct_id)).balance < float(withdraw):
                    return "Insufficient funds.", 422
            # pass
            if deposit is not None:
                if int(deposit) > 0 and deposit is not None:
                    acct_service.deposit(int(acct_id), int(deposit))
            if withdraw is not None:
                if int(withdraw) > 0 and withdraw is not None:
                    acct_service.withdraw(int(acct_id), int(withdraw))
            app.logger.info(f'Account ID: {acct_id} balance was changed.')
            return f"Balance was successfully updated\nNew balance: {acct_service.get_acct_by_acct_id(int(acct_id)).balance}", 200
        except AccountNotFoundError as e:
            return e.message, 404
        except AttributeError:
            return "Client/Account not found.\nPlease enter valid information.", 404

    @app.patch('/clients/<client_id>/accounts/<acct_id>/transfer/<destination>')
    def transfer(client_id: str, acct_id: str, destination: str):
        amount = request.args.get('amount')
        try:
            if acct_service.get_acct_by_acct_id(int(acct_id)).client_id != int(
                    client_id) or acct_service.get_acct_by_acct_id(int(destination)).client_id != int(client_id):
                return "Account does not exist for that client.", 404
            if acct_service.get_acct_by_acct_id(int(acct_id)).balance < float(amount):
                return "Insufficient funds.", 422
            acct_service.transfer(int(client_id), int(acct_id), int(destination), float(amount))
            app.logger.info(f'transfer from account ID: {acct_id} to account ID: {destination}')
            return "Transfer was successful", 200
        except AccountNotFoundError as e:
            return e.message, 404
        except AttributeError:
            return "Client/Account not found.\nPlease enter valid information.", 404
