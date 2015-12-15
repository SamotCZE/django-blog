from django.test import TestCase
from django.utils import timezone
from unittest import mock

from model_mommy import mommy

from blog.models import Post, Comment


class PostTest(TestCase):

    def test_post_creation(self):
        post = mommy.make(Post)
        self.assertTrue(isinstance(post, Post))
        self.assertEqual(post.__str__(), post.title)
        self.assertIsNone(post.published_date)

    def test_post_publish(self):
        testtime = timezone.now()

        with mock.patch('django.utils.timezone.now') as mock_now:
            post = mommy.make(Post)
            mock_now.return_value = testtime
            post.publish()

        self.assertEqual(testtime, post.published_date)

    def test_approved_comments(self):
        post = mommy.make(Post)
        comment = mommy.make(Comment)
        comment.approved_comment = True
        comment.save()
        post.comments.add(comment)
        approved_posts = post.approved_comments()

        self.assertTrue(approved_posts.count() > 0)


class CommentTest(TestCase):

    def test_comment_creation(self):
        comment = mommy.make(Comment)
        self.assertTrue(isinstance(comment, Comment))
        self.assertEqual(comment.__str__(), comment.text)
        self.assertFalse(comment.approved_comment)

    def test_comment_approve(self):
        comment = mommy.make(Comment)
        comment.approve()
        self.assertTrue(comment.approved_comment)