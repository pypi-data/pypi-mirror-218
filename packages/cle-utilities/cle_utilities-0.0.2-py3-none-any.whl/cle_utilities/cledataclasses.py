import json 

class CleHeader:
    def __init__(self, ApplicationID, ServiceName, ComponentName, Timestamp, TransactionDomain, TransactionType,
                 TransactionID, Hostname, BusinessID, ApplicationDomain, BusinessID2=None):
        self.ApplicationID = ApplicationID
        self.ServiceName = ServiceName
        self.ComponentName = ComponentName
        self.Hostname = Hostname
        self.Timestamp = Timestamp
        self.TransactionDomain = TransactionDomain
        self.TransactionType = TransactionType
        self.TransactionID = TransactionID
        self.BusinessID = BusinessID
        self.ApplicationDomain = ApplicationDomain
        if BusinessID2:
            self.BusinessID2 = BusinessID2

    def __str__(self):
        return json.dumps(self.__dict__)
    

class CleLogRequest:
    def __init__(self, header, LogLevel, TimeDuration=None, Category=None, Messages=None, Status=None,
                 TransactionBefore=None, TransactionAfter=None, DataEncoding=None):
        self.Header = header
        if TimeDuration:
            self.TimeDuration = TimeDuration
        if Category:
            self.Category = Category
        if Messages:
            self.Messages = Messages
        if Status:
            self.Status = Status
        if TransactionBefore:
            self.TransactionBefore = TransactionBefore
        if TransactionAfter:
            self.TransactionAfter = TransactionAfter
        self.LogLevel = LogLevel
        if DataEncoding:
            self.DataEncoding = DataEncoding


class ExceptionHeaders:
    def __init__(self, true_client_ip=None, client_ip=None, x_forwarder_for=None, access_control_allow_origin=None):
        self.headers = {"True-Client-IP":true_client_ip, "Client-IP":client_ip, "X-Forwarder-FOR":x_forwarder_for, "Access-Control-Allow-Origin":access_control_allow_origin}


class ExceptionData:
    def __init__(self, headers, error_details, log_level=None, date_time=None, correlation_id=None, call_stack=None, user_id=None, service_id=None, service_instance=None, data=None):
        self.headers = headers
        self.LogLevel = log_level
        self.DateTime = date_time
        self.CorrelationID = correlation_id
        self.ErrorDetails = error_details
        self.CallStack = call_stack
        self.UserID = user_id
        self.ServiceID = service_id
        self.ServiceInstance = service_instance
        self.Data = data

    def __str__(self):
        json.dumps(self.__dict__)


class CleExceptionRequest:
    def __init__(self, header, Category, ExceptionType, Severity, Code, TransactionData, ExceptionData, Message = None, MessagesNVP = None, ReplyDestination = None, 
                 ReplayCount = None, DataEncoding = None, MessageHeader = None, SendExactMessage = None, IssueGroup = None):
        self.Header = header
        self.Category = Category
        self.Type = ExceptionType
        self.Severity = Severity
        self.Code = Code
        if Message:
            self.Message = Message
        if MessagesNVP:
            self.MessagesNVP = MessagesNVP
        if ReplyDestination:
            self.ReplyDestination = ReplyDestination
        if ReplayCount:
            self.ReplayCount = ReplayCount
        else:
            self.ReplayCount = "0"
        self.TransactionData = TransactionData
        self.DumpAnalysis = ExceptionData
        if DataEncoding:
            self.DataEncoding = DataEncoding
        if MessageHeader:
            self.MessageHeader = MessageHeader
        if SendExactMessage:
            self.SendExactMessage = SendExactMessage
        else:
            self.SendExactMessage = "N"
        if IssueGroup:
            self.IssueGroup = IssueGroup