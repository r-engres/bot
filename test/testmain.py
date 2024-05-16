import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import src.main as bot

from unittest.mock import Mock, patch

class TestSubmission(unittest.TestCase):

    def setUp(self):
        self.mock_submission = Mock()
        self.mock_reddit = Mock()
        self.mock_remove = patch.object(bot, 'remove').start()
        self.mock_approve = patch.object(bot, 'approve').start()

        self.mock_submission.subreddit.name = "engineeringresumes"

    def tearDown(self):
        self.mock_submission.reset_mock()
        self.mock_reddit.reset_mock()
        self.mock_remove.stop()
        self.mock_approve.stop()

    def test_process_with_question_flair(self):
        self.mock_submission.approved = False
        self.mock_submission.link_flair_text = "Question"
        with patch.object(bot, 'extract_width') as mock_extract_width:
            bot.process(self.mock_submission)

        self.mock_remove.assert_not_called()
        self.mock_approve.assert_not_called()
        mock_extract_width.assert_not_called()
        pass

    def test_process_with_success_story_flair(self):
        self.mock_submission.approved = False
        self.mock_submission.link_flair_text = "Success Story!"
        with patch.object(bot, 'extract_width') as mock_extract_width:
            bot.process(self.mock_submission)

        self.mock_remove.assert_not_called()
        self.mock_approve.assert_not_called()
        mock_extract_width.assert_not_called()
        pass

    def test_process_with_meta_flair(self):
        self.mock_submission.approved = False
        self.mock_submission.link_flair_text = "Meta"
        with patch.object(bot, 'extract_width') as mock_extract_width:
            bot.process(self.mock_submission)

        self.mock_remove.assert_not_called()
        self.mock_approve.assert_not_called()
        mock_extract_width.assert_not_called()
        pass

    def test_already_approved(self):
        self.mock_submission.approved = True
        with patch.object(bot, 'extract_width') as mock_extract_width:
            bot.process(self.mock_submission)

        self.mock_remove.assert_not_called()
        self.mock_approve.assert_not_called()
        mock_extract_width.assert_not_called()
        pass

    def test_process_remove(self):
        self.mock_submission.approved = False
        self.mock_submission.selftext = "width=30" #Under required size
        bot.process(self.mock_submission)

        self.mock_remove.assert_called_once_with(self.mock_submission, 30)
        self.mock_approve.assert_not_called()
        pass

    def test_process_approve(self):
        self.mock_submission.approved = False
        self.mock_submission.link_flair = "test"
        self.mock_submission.selftext = "width=3000&" #Over required size
        bot.process(self.mock_submission)

        self.mock_approve.assert_called_once_with(self.mock_submission, 3000)
        self.mock_remove.assert_not_called()
        pass

    def test_extract_width_invalid(self):
        self.mock_submission.selftext = "INVALID"
        assert bot.extract_width(self.mock_submission.selftext) == -1
        pass

    def test_extract_width_valid(self):
        self.mock_submission.selftext = "width=30"
        assert bot.extract_width(self.mock_submission.selftext) == 30
        pass

if __name__ == '__main__':
    unittest.main()

