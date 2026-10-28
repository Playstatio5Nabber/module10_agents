# Exercise 1

1. The two classes are: OrderLookup and SupportChatbot.
2. One object of each class in main.py: order_tool is an OrderLookup object, and bot is a SupportChatbot object.
3. Every attribute of SupportChatbot: self.name, self.instructions, self.order_tool, and self.history.
4. Every method of OrderLookup: __init__, find_order_id, and find_status.
5. The line in chatbot.py that is the composition: self.order_tool = order_tool
6. In bot.respond("hello"), self is: bot.