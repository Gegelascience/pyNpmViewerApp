import json
import typing
import urllib.error
import urllib.parse
import urllib.request
from email.message import Message
import base64


class ResponseWrapper(typing.NamedTuple):
    body: bytes | str
    headers: Message
    status: int
    error_count: int = 0

    def text(self) -> str:
        if not isinstance(self.body,str):
            return self.body.decode(self.headers.get_content_charset("utf-8"))
        else:
            return self.body
        
    def raw(self):
        return self.body

    def json(self) -> typing.Any:
        """
        Decode body's JSON.

        Returns:
            Pythonic representation of the JSON object
        """
        bodyToParse = self.text()
        try:
            output = json.loads(bodyToParse)
        except json.JSONDecodeError:
            output = ""
        return output


def getBasicAuthorizationToken(user:str,mdp:str)-> str:
    # ajout de l'authentification
    baseAuthCred = user + "/token:" + mdp
    baseAuthByte = baseAuthCred.encode('utf-8')
    nearlyOk = base64.encodebytes(baseAuthByte)

    # on découpe la chaine binaire suivant le caractère binaire equivalent au \n
    listOk = nearlyOk.split(b'\n')
	
    # on recupère le token au format binaire
    base64Cred=b''
    for elem in listOk:
        base64Cred = base64Cred + elem

    base64string = base64Cred.decode('utf-8')
    return base64string


def requestWrapper(
    url: str,
    data: dict = None,
    params: dict = None,
    headers: dict = None,
    method: str = "GET",
    dataType: str = "json",
    error_count: int = 0,
) -> ResponseWrapper:
    if not url.casefold().startswith("http"):
        raise urllib.error.URLError("Incorrect and possibly insecure protocol in url")
    method = method.upper()
    request_data = None
    headers = headers or {}
    data = data or {}
    params = params or {}
    headers = {"Accept": "application/json", **headers}

    if method == "GET":
        params = {**params, **data}
        data = None

    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True, safe="/")

    if data:
        if dataType:
            dataType = dataType.lower()
            if  dataType =="json":
                request_data = json.dumps(data).encode()
                headers["Content-Type"] = "application/json; charset=UTF-8"
            elif dataType =="binary":
                request_data = data
            else:
               request_data = urllib.parse.urlencode(data).encode() 
        else:
            request_data = urllib.parse.urlencode(data).encode()

    httprequest = urllib.request.Request(url, data=request_data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(httprequest) as httpresponse:
            response = ResponseWrapper(
                headers=httpresponse.headers,
                status=httpresponse.status,
                body=httpresponse.read(),
            )
    except urllib.error.HTTPError as e:
        response = ResponseWrapper(
            body=str(e.reason),
            headers=e.headers,
            status=e.code,
            error_count=error_count + 1,
        )

    return response