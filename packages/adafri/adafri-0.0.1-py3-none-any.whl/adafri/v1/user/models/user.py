from utils.utils import JsonEncoder, DictUtils, Crypto
from .user_fields import UserFields, UserFieldProps
from typing import List
from typing import Any
from dataclasses import dataclass
import json
import pydash

@dataclass
class Account:
    canManageClients: bool
    childs: List[object]
    currenyCode: str
    customerId: int
    dateTimeZone: str
    name: str
    testAccount: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Account':
        _canManageClients = DictUtils.pick(obj, "canManageClients", bool)
        _childs = [y for y in DictUtils.pick(obj, "childs", list)]
        _currenyCode = str(DictUtils.pick(obj, "currenyCode", str))
        _customerId = int(DictUtils.pick(obj, "customerId", int))
        _dateTimeZone = str(DictUtils.pick(obj, "dateTimeZone",str))
        _name = str(DictUtils.pick(obj, "name", str))
        _testAccount = bool(DictUtils.pick(obj, "testAccount", bool))
        return Account(_canManageClients, _childs, _currenyCode, _customerId, _dateTimeZone, _name, _testAccount)

@dataclass
class Country:
    areaCodes: List[object]
    dialCode: str
    flagClass: str
    htmlId: str
    iso2: str
    name: str
    placeHolder: str
    priority: int

    @staticmethod
    def from_dict(obj: Any) -> 'Country':
        _areaCodes = [y for y in DictUtils.pick(obj, "areaCodes", list)]
        _dialCode = str(DictUtils.pick(obj, "dialCode", str))
        _flagClass = str(DictUtils.pick(obj, "flagClass",str))
        _htmlId = str(DictUtils.pick(obj, "htmlId", str))
        _iso2 = str(DictUtils.pick(obj, "iso2", str))
        _name = str(DictUtils.pick(obj, "name", str))
        _placeHolder = str(DictUtils.pick(obj, "placeHolder", str))
        _priority = int(DictUtils.pick(obj, "priority", int))
        return Country(_areaCodes, _dialCode, _flagClass, _htmlId, _iso2, _name, _placeHolder, _priority)

@dataclass
class Credential:
    refresh_token: str
    scopes: List[str]
    token: str
    token_uri: str

    @staticmethod
    def from_dict(obj: Any) -> 'Credential':
        _refresh_token = str(DictUtils.pick(obj, "refresh_token", str))
        _scopes = [y for y in DictUtils.pick(obj, "scopes", list)]
        _token = str(DictUtils.pick(obj, "token", str))
        _token_uri = str(DictUtils.pick(obj, "token_uri", str))
        return Credential(_refresh_token, _scopes, _token, _token_uri)

@dataclass
class DeviceInfo:
    browser: str
    browser_version: str
    device: str
    os: str
    os_version: str
    userAgent: str

    @staticmethod
    def from_dict(obj: Any) -> 'DeviceInfo':
        _browser = str(DictUtils.pick(obj, "browser", str))
        _browser_version = str(DictUtils.pick(obj, "browser_version", str))
        _device = str(DictUtils.pick(obj, "device", str))
        _os = str(DictUtils.pick(obj, "os", str))
        _os_version = str(DictUtils.pick(obj, "os_version", str))
        _userAgent = str(DictUtils.pick(obj, "userAgent", str))
        return DeviceInfo(_browser, _browser_version, _device, _os, _os_version, _userAgent)

@dataclass
class PartenerData:
    id: str
    text: str

    @staticmethod
    def from_dict(obj: Any) -> 'PartenerData':
        _id = str(DictUtils.pick(obj, "id", str))
        _text = str(DictUtils.pick(obj, "text", str))
        return PartenerData(_id, _text)

@dataclass
class PhoneInfo:
    countryCode: str
    dialCode: str
    e164Number: str
    internationalNumber: str
    nationalNumber: str
    number: str

    @staticmethod
    def from_dict(obj: Any) -> 'PhoneInfo':
        _countryCode = str(DictUtils.pick(obj, "countryCode", str))
        _dialCode = str(DictUtils.pick(obj, "dialCode", str))
        _e164Number = str(DictUtils.pick(obj, "e164Number", str))
        _internationalNumber = str(DictUtils.pick(obj, "internationalNumber", str))
        _nationalNumber = str(DictUtils.pick(obj, "nationalNumber", str))
        _number = str(DictUtils.pick(obj, "number", str))
        return PhoneInfo(_countryCode, _dialCode, _e164Number, _internationalNumber, _nationalNumber, _number)

@dataclass
class PlateformRole:
    id: str
    partenerData: PartenerData
    text: str

    @staticmethod
    def from_dict(obj: Any) -> 'PlateformRole':
        _id = str(DictUtils.pick(obj, "id", str))
        _partenerData = PartenerData.from_dict(DictUtils.pick(obj, "partenerData", dict))
        _text = str(DictUtils.pick(obj, "text", str))
        return PlateformRole(_id, _partenerData, _text)

@dataclass
class User:
    account_value: int
    accounts: List[Account]
    addresse: str
    auth_code: str
    authorizedPush: bool
    country: Country
    credentials: List[Credential]
    deviceInfo: DeviceInfo
    displayName: str
    email: str
    entrepriseName: str
    entrepriseUrl: str
    first_name: str
    hasApprouvedPolicy: bool
    invitedAccounts: List[object]
    isConnectWithMailAndPassword: bool
    isCorporate: bool
    isDesktopDevice: bool
    isMobile: bool
    isParticular: bool
    isTablet: bool
    last_name: str
    linkedAccounts: List[object]
    ownedAccounts: List[object]
    phoneInfo: PhoneInfo
    photoURL: str
    plateformRole: PlateformRole
    postal: str
    profileCompleted: bool
    showPushToken: bool
    telephone: str
    token: List[str]
    uid: str
    user_type: str
    password: str
    provider: str
    collection_name = 'users';

    
    
    @staticmethod
    def from_dict(obj: Any) -> 'User':
        _account_value = DictUtils.pick(obj, "account_value", int)
        _accounts = [Account.from_dict(y) for y in DictUtils.pick(obj, "accounts", list)]
        _addresse = DictUtils.pick(obj, UserFields.address, str) 
        _auth_code = DictUtils.pick(obj, "auth_code", str)
        _authorizedPush = DictUtils.pick(obj, UserFields.authorizedPush, bool)
        _country = Country.from_dict(DictUtils.pick(obj, "country", dict))
        _credentials = [Credential.from_dict(y) for y in DictUtils.pick(obj, "credentials", list)]
        _deviceInfo = DeviceInfo.from_dict(DictUtils.pick(obj, UserFields.deviceInfo, dict))
        _displayName = DictUtils.pick(obj, UserFields.displayName, str)
        _email = DictUtils.pick(obj, UserFields.email, str)
        _entrepriseName = DictUtils.pick(obj, UserFields.entrepriseName, str)
        _entrepriseUrl = DictUtils.pick(obj, UserFields.entrepriseUrl, str)
        _first_name = DictUtils.pick(obj, UserFields.firstName, str)
        _hasApprouvedPolicy = DictUtils.pick(obj, UserFields.hasApprouvedPolicy, str)
        _invitedAccounts = [y for y in DictUtils.pick(obj, 'invitedAccounts', list)]
        _isConnectWithMailAndPassword =  DictUtils.pick(obj, UserFields.isConnectWithMailAndPassword, bool)
        _isCorporate = DictUtils.pick(obj,'isCorporate', bool)
        _isDesktopDevice = DictUtils.pick(obj, "isDesktopDevice",bool)
        _isMobile = DictUtils.pick(obj, "isMobile", bool)
        _isParticular = DictUtils.pick(obj, "isParticular", bool)
        _isTablet = DictUtils.pick(obj, "isTablet", bool)
        _last_name = DictUtils.pick(obj, UserFields.lastName, str)
        _linkedAccounts = [y for y in DictUtils.pick(obj, "linkedAccounts", list)]
        _ownedAccounts = [y for y in DictUtils.pick(obj, "ownedAccounts", list)]
        _phoneInfo = PhoneInfo.from_dict(DictUtils.pick(obj, "phoneInfo", dict))
        _photoURL = DictUtils.pick(obj, UserFields.photoURL, str)
        _plateformRole = PlateformRole.from_dict(DictUtils.pick(obj, "plateformRole", dict))
        _postal = DictUtils.pick(obj, UserFields.postalCode, str)
        _profileCompleted = DictUtils.pick(obj, UserFields.profileCompleted, bool)
        _showPushToken = DictUtils.pick(obj, UserFields.showPushToken, bool)
        _telephone = DictUtils.pick(obj, UserFields.telephone, str)
        _token = [y for y in DictUtils.pick(obj, UserFields.token, list)]
        _uid = DictUtils.pick(obj, UserFields.uid, str)
        _user_type = DictUtils.pick(obj, "user_type", str)
        _password = DictUtils.pick(obj, UserFields.password, str)
        _provider = DictUtils.pick(obj, UserFields.provider, str)
        return User(_account_value, _accounts, _addresse, _auth_code, _authorizedPush, _country, _credentials, _deviceInfo, _displayName, _email, _entrepriseName, _entrepriseUrl, _first_name, _hasApprouvedPolicy, _invitedAccounts, _isConnectWithMailAndPassword, _isCorporate, _isDesktopDevice, _isMobile, _isParticular, _isTablet, _last_name, _linkedAccounts, _ownedAccounts, _phoneInfo, _photoURL, _plateformRole, _postal, _profileCompleted, _showPushToken, _telephone, _token, _uid, _user_type, _password, _provider)
    
    @staticmethod
    def generate_model():
        user = {};
        for k in DictUtils.get_keys(UserFieldProps):
            _key_ = 'default_value';
            user[k] = UserFieldProps[k][_key_];
        return user;


    def to_json(self, fields=None):
        if fields is None or type(fields) is not list:
            return json.loads(JsonEncoder().encode(self));
    
        return pydash.pick(json.loads(JsonEncoder().encode(self)), fields)
    


