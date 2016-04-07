import json
import logging
import random

from textblob import TextBlob
from text_corpus import TextCorpus

logger = logging.getLogger(__name__)


class RtmEventHandler(object):
    def __init__(self, slack_clients, msg_writer, trump_corpus):
        self.clients = slack_clients
        self.msg_writer = msg_writer
        self.trump_corpus = trump_corpus

    def handle(self, event):

        if 'type' in event:
            self._handle_by_type(event['type'], event)

    def _handle_by_type(self, event_type, event):
        # See https://api.slack.com/rtm for a full list of events
        if event_type == 'error':
            # error
            self.msg_writer.write_error(event['channel'], json.dumps(event))
        elif event_type == 'message':
            # message was sent to channel
            self._handle_message(event)
        elif event_type == 'channel_joined':
            # you joined a channel
            self.msg_writer.send_message(event['channel'], "Let's make America great again!")
        elif event_type == 'group_joined':
            # you joined a private group
            self.msg_writer.write_help_message(event['channel'])
        else:
            pass

    def _handle_message(self, event):
        # Filter out messages from the bot itself
        if not self.clients.is_message_from_me(event['user']):

            msg_txt = event['text']

            if self.clients.is_bot_mention(msg_txt):
                txt_b = TextBlob(msg_txt)
                for sentence in txt_b.sentences:
                    for tag in sentence.tags:
                        print tag
                        response = self.trump_corpus.gen_text([tag[0]], 1)
                        if response is not None:
                            self.msg_writer.send_message(event['channel'], response)
                            return

                # No seed match, so ask a question instead
                question = random.choice(random.choice(self.trump_corpus.nouns_to_quest.values()))
                self.msg_writer.send_message(event['channel'], question.raw)