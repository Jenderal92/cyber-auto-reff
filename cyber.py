import json
import time
import requests
from eth_account import Account
from eth_account.messages import encode_defunct

headers = {
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
    'Content-Type': 'application/json',
    'Origin': 'https://cyber.deform.cc',
    'Privy-App-Id': 'clphlvsh3034xjw0fvs59mrdc',
    'Privy-Ca-Id': '649814d3-98c4-4a73-a28d-ad39c448fad0',
    'Privy-Client': 'react-auth:1.68.0-beta-20240603143655',
    'Referer': 'https://cyber.deform.cc/',
    'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Linux"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def generate_eth_account():
    account = Account.create()
    print("\n• Generate Address")
    print("New Ethereum Address:" + account.address)
    print("Private Key:" + account._private_key.hex())
    time.sleep(3)
    return account

def init_authentication():
    account = generate_eth_account()
    print("\n• Get Nonce ")
    url_init = "https://auth.privy.io/api/v1/siwe/init"
    data_init = {"address": account.address}
    response_init = requests.post(url_init, headers=headers, data=json.dumps(data_init)).json()
    nonce = response_init['nonce']
    issued_at = response_init['expires_at']
    print("[-] Nonce :"+ nonce + " " + "Expires at : " + issued_at)
    time.sleep(3)
    return account, nonce, issued_at

def authenticate():
    account, nonce, issued_at = init_authentication()
    print("• Auth Login")
    url_auth = "https://auth.privy.io/api/v1/siwe/authenticate"
    message = (
        "cyber.deform.cc wants you to sign in with your Ethereum account:\n" +
        account.address + "\n\nBy signing, you are proving you own this wallet and logging in. "
        "This does not initiate a transaction or cost any fees.\n\nURI: https://cyber.deform.cc\n"
        "Version: 1\nChain ID: 1\nNonce: " + nonce + "\n"
        "Issued At: " + issued_at + "\nResources:\n- https://privy.io"
    )
    message_encoded = encode_defunct(text=message)
    signature = Account.sign_message(message_encoded, private_key=account._private_key)
    data = {
        "message": message,
        "signature": signature.signature.hex(),
        "chainId": "eip155:1",
        "walletClientType": "metamask",
        "connectorType": "injected"
    }
    response = requests.post(url_auth, headers=headers, data=json.dumps(data)).json()
    token = response["token"]
    print("[-] Token :"+ token)
    time.sleep(3)
    return token

def get_user_auth():
    token = authenticate()
    print("• Get UserAuth")
    api_auth = "https://api.deform.cc/"
    data = {
        "operationName": "UserLogin",
        "variables": {
            "data": {
                "externalAuthToken": token
            }
        },
        "query": "mutation UserLogin($data: UserLoginInput!) {\n  userLogin(data: $data)\n}"
    }

    response = requests.post(api_auth, headers=headers, data=json.dumps(data)).json()
    datane = response['data']['userLogin']
    print("[-] Bearer :"+ datane)
    time.sleep(3)
    return datane, api_auth

def check_id_campaign():
    datane, api_auth = get_user_auth()
    print("• Check Campaign")
    headers2 = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': 'Bearer ' + datane
    }
    data = {
        "operationName": "Campaign",
        "variables": {
            "campaignId": "0c5229f6-de83-43e2-a64c-7d4306b82084"
        },
        "query": (
            "query Campaign($campaignId: String!) {\n"
            "  campaign(id: $campaignId) {\n"
            "    id\n"
            "    activities {\n"
            "      id\n"
            "      createdAt\n"
            "      updatedAt\n"
            "      startDateTimeAt\n"
            "      endDateTimeAt\n"
            "      title\n"
            "      description\n"
            "      type\n"
            "      identityType\n"
            "      recurringPeriod {\n"
            "        count\n"
            "        type\n"
            "        __typename\n"
            "      }\n"
            "      recurringMaxCount\n"
            "      properties\n"
            "      records {\n"
            "        id\n"
            "        status\n"
            "        createdAt\n"
            "        __typename\n"
            "      }\n"
            "      reward {\n"
            "        id\n"
            "        quantity\n"
            "        type\n"
            "        __typename\n"
            "      }\n"
            "      nft {\n"
            "        id\n"
            "        tokenId\n"
            "        name\n"
            "        description\n"
            "        image\n"
            "        properties\n"
            "        mintPrice\n"
            "        platformFee\n"
            "        maxSupply\n"
            "        maxMintCountPerAddress\n"
            "        nftContract {\n"
            "          id\n"
            "          address\n"
            "          type\n"
            "          chainId\n"
            "          __typename\n"
            "        }\n"
            "        __typename\n"
            "      }\n"
            "      __typename\n"
            "    }\n"
            "    standaloneActivities {\n"
            "      id\n"
            "      __typename\n"
            "    }\n"
            "    missions {\n"
            "      id\n"
            "      createdAt\n"
            "      updatedAt\n"
            "      startDateTimeAt\n"
            "      endDateTimeAt\n"
            "      title\n"
            "      description\n"
            "      coverPhotoUrl\n"
            "      recurringPeriod {\n"
            "        count\n"
            "        type\n"
            "        __typename\n"
            "      }\n"
            "      recurringMaxCount\n"
            "      properties\n"
            "      rewards {\n"
            "        id\n"
            "        quantity\n"
            "        type\n"
            "        __typename\n"
            "      }\n"
            "      records {\n"
            "        id\n"
            "        status\n"
            "        createdAt\n"
            "        __typename\n"
            "      }\n"
            "      activities {\n"
            "        id\n"
            "        __typename\n"
            "      }\n"
            "      __typename\n"
            "    }\n"
            "    __typename\n"
            "  }\n"
            "}"
        )
    }
    response = requests.post(api_auth, headers=headers2, data=json.dumps(data)).json()
    activities = response['data']['campaign']['activities']
    activity_list = [activity['title'] + ":" + activity['id'] for activity in activities]
    time.sleep(3)
    return activity_list, headers2, api_auth

def verify_Referral():
    activity_list, headers2, api_auth = check_id_campaign()
    print("• Verify Referral")
    for activity in activity_list:
        if "Campaign registration" in activity:
            activity_id = activity.split(":")[1]
            data = {
                "operationName": "VerifyActivity",
                "variables": {
                    "data": {
                        "activityId": activity_id,
                        "metadata": {
                            "referralCode": ref_code
                        }
                    }
                },
                "query": (
                    "mutation VerifyActivity($data: VerifyActivityInput!) {\n"
                    "  verifyActivity(data: $data) {\n"
                    "    record {\n"
                    "      id\n"
                    "      status\n"
                    "      createdAt\n"
                    "      __typename\n"
                    "    }\n"
                    "    __typename\n"
                    "  }\n"
                    "}"
                )
            }
            response = requests.post(api_auth, headers=headers2, data=json.dumps(data))
            print(f"[-] {activity.split(':')[0]} => Done")
            time.sleep(3)
            return activity_list, headers2, api_auth

def verify_task():
    activity_list, headers2, api_auth = verify_Referral()
    print("\n• Verify Task")
    ids_to_check = [
        "Visit Cyber Staking Website",
        "Learn more about Cyber Mainnet Staking",
        "Check in to Staking Party every day"
    ]
    
    for activity in activity_list:
        for title in ids_to_check:
            if title in activity:
                activity_id = activity.split(":")[1]
                data = {
                    "operationName": "VerifyActivity",
                    "variables": {
                        "data": {
                            "activityId": activity_id
                        }
                    },
                    "query": (
                        "mutation VerifyActivity($data: VerifyActivityInput!) {\n"
                        "  verifyActivity(data: $data) {\n"
                        "    record {\n"
                        "      id\n"
                        "      status\n"
                        "      createdAt\n"
                        "      __typename\n"
                        "    }\n"
                        "    __typename\n"
                        "  }\n"
                        "}"
                    )
                }
                response = requests.post(api_auth, headers=headers2, data=json.dumps(data))
                print(f"[-] {activity.split(':')[0]} => Done")
                time.sleep(3)
 
if __name__ == "__main__":
    print("\nCyber Mainnet - Auto Referral\n")
    ref_code_file = input("Input list file => ")
    with open(ref_code_file, "r") as file:
        ref_code = file.read().strip()
    
    ref_total = input("How Many Referrals You Need => ")
    
    for i in range(int(ref_total)):
        print(f"\nReferral Code : {ref_code} => [{i}]")
        verify_task()