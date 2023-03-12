import grpc
from concurrent import futures
import payment_gateway_pb2_grpc
from payment_gateway_pb2 import(TransactionRequest,CardDetails,TransactionResponse,ResponseType)


Card_database = [
    CardDetails(CardNumber= "4592078017232006",ExpiryMonth=12,ExpiryYear=29,NameOnCard= "Advait Chandorkar",CVV = 981,OnlineTransactionsEnabled = True,StaticTransactionPassword= "babaramdev",BankBalance = 405121),
    CardDetails(CardNumber= "4592000025854881",ExpiryMonth=2,ExpiryYear=35,NameOnCard= "Vijay Sharma",CVV = 364,OnlineTransactionsEnabled = False,StaticTransactionPassword= "swaminityanand",BankBalance = 78914)
]

class TransactionService(payment_gateway_pb2_grpc.TransactionServicer):
    def Transact(self, request, context):
        for i in Card_database:
            if request.CardNumber != i.CardNumber :
                if (i == (len(Card_database)-1)):
                    return TransactionResponse(response = ResponseType.WrongCardNumber,BankBalance = None)
                if request.ExpiryMonth != i.ExpiryMonth:
                    if 1:
                        return TransactionResponse(response = ResponseType.WrongExpiryMonth,BankBalance = None)
                        if request.ExpiryYear != i.ExpiryYear:
                            if 1:
                                return TransactionResponse(response = ResponseType.WrongExpiryYear,BankBalance = None)
                                if request.NameOnCard != i.NameOnCard:
                                    if 1:
                                        return TransactionResponse(response = ResponseType.WrongNameOnCard,BankBalance = None)
                                        if request.CVV != i.CVV:
                                            if 1:
                                                return TransactionResponse(response = ResponseType.WrongCVV,BankBalance = None)  
                                                if request.OnlineTransactionsEnabled != i.OnlineTransactionsEnabled:
                                                    if 1:
                                                        return TransactionResponse(response = ResponseType.OnlineTransactionsNotEnabled,BankBalance = None)       
                                                        if request.StaticTransactionPassword != i.StaticTransactionPassword:
                                                            if 1:
                                                                return TransactionResponse(response = ResponseType.StaticTransactionPassword,BankBalance = None)     
                                                                if request.BankBalance < i.BankBalance:
                                                                    Card_database[i].BankBalance = Card_database[i].BankBalance - 1
                                                                    return TransactionResponse(response = ResponseType.SuccessfulTransaction,BankBalance = Card_database[i].BankBalance) 


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    payment_gateway_pb2_grpc.add_TransactionServicer_to_server(TransactionService,server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()