import json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle

from EdgeGPT.chathub import ChatHubRequest


class chat():
    async def newBot(self):
        self.bot = await Chatbot.create()

    async def ask(self, prompt):
        response = await self.bot.ask(prompt=prompt,
                                      conversation_style=ConversationStyle.creative,
                                      simplify_response=True)
        return response["text"]

    def ask_stream(self, prompt):
        response = self.bot.ask_stream(prompt=prompt,
                                       conversation_style=ConversationStyle.creative)
        return response

    def getConversation(self):
        conversation_id = self.bot.chat_hub.request.conversation_id
        conversation_signature = self.bot.chat_hub.request.conversation_signature
        client_id = self.bot.chat_hub.request.client_id
        invocation_id = self.bot.chat_hub.request.invocation_id
        return {
            "conversation_id": conversation_id,
            "conversation_signature": conversation_signature,
            "client_id": client_id,
            "invocation_id": invocation_id,
        }

    def loadConversation(self, conversation):
        self.bot.chat_hub.request = ChatHubRequest(
            conversation_signature=conversation["conversation_signature"],
            client_id=conversation["client_id"],
            conversation_id=conversation["conversation_id"],
            invocation_id=conversation["invocation_id"],
        )


def inQueryShowing(resp):
    splited = resp.split("\n```json\n")
    progress = splited[0]
    splited = splited[1].split("\n```\n")
    cited = json.loads(splited[0])["web_search_results"]
    generated = splited[1]
    # print(len(cited))
    splited = generated.split("\n[")[-1].split("\n")
    generated = ""
    for i in splited[1:]:
        generated += i
    return progress, cited, generated


def cleanResp(text):
    clean = ""
    # print(text)
    for each in text.split("[^"):
        # print(each)
        if "^]" in each:
            clean += each[each.find("^]") + 2:]
            # print(each.find("^]"), each)
        else:
            clean += each
    clean = clean.replace("\n- ", "<!--List Object-->").replace("\n", "").replace("<!--List Object-->", "\n· ").replace(
        "**", " ").replace("*", '"')
    return clean


def simplifyResp(response):
    global message
    for msg in reversed(response["item"]["messages"]):
        if msg.get("adaptiveCards") and msg["adaptiveCards"][0]["body"][
            0
        ].get("text"):
            message = msg
            break
    suggestions = [
        suggestion["text"]
        for suggestion in message.get("suggestedResponses", [])
    ]
    adaptive_cards = message.get("adaptiveCards", [])
    adaptive_text = (
        adaptive_cards[0]["body"][0].get("text") if adaptive_cards else None
    )
    sources = (
        adaptive_cards[0]["body"][0].get("text") if adaptive_cards else None
    )
    sources_text = (
        adaptive_cards[0]["body"][-1].get("text")
        if adaptive_cards
        else None
    )
    return {
        "text": message["text"],
        "author": message["author"],
        "sources": sources,
        "sources_text": sources_text,
        "suggestions": suggestions,
        "messages_left": response["item"]["throttling"][
                             "maxNumUserMessagesInConversation"
                         ]
                         - response["item"]["throttling"].get(
            "numUserMessagesInConversation", 0
        ),
        "max_messages": response["item"]["throttling"][
            "maxNumUserMessagesInConversation"
        ],
        "adaptive_text": adaptive_text,
    }


def chaos2text(i):
    if not i[0] and "```" in i[1]:
        # print("state 1")
        return cleanResp(inQueryShowing(i[1])[2])
    elif i[0]:
        # print("state 2")
        temp = simplifyResp(i[1])
        return cleanResp(temp["text"])
    else:
        # print("state 3")
        # print(i)
        return i[1]
