from __future__ import absolute_import, unicode_literals

from unittest import TestCase

from invoke_release import tasks


class TestTasks(TestCase):
    """
    At a later point, we will write some actual tests. This project is difficult to test with automated tests, and
    we largely rely on manual tests.
    """

    def test_case_sensitive_regular_file_exists(self):
        assert tasks._case_sensitive_regular_file_exists(__file__) is True
        assert tasks._case_sensitive_regular_file_exists(__file__.upper()) is False
        assert tasks._case_sensitive_regular_file_exists(__file__ + '.bogus') is False

    def test_get_version_to_bump_decides_correctly_when_different_multiple_commits(self):

        changelog_message = [
            '[PATCH] A patch-commit message.\n',
            '[MINOR] A minor-commit message.\n',
            '[MAJOR] A major-commit message.\n',
        ]

        version_to_bump = tasks._get_version_to_bump(changelog_message)

        assert version_to_bump == tasks.MAJOR_TAG

    def test_get_version_to_bump_decides_correctly_when_single_commit(self):

        changelog_message = [
            '[MINOR] A minor-commit message.\n',
        ]

        version_to_bump = tasks._get_version_to_bump(changelog_message)

        assert version_to_bump == tasks.MINOR_TAG

    def test_get_version_to_bump_returns_none_if_commit_does_not_have_tag(self):

        changelog_message = [
            '[MINOR] A minor-commit message.\n',
            'A commit message with no tag.\n',
        ]

        version_to_bump = tasks._get_version_to_bump(changelog_message)

        assert version_to_bump is None

    def test_suggest_version_is_correct_for_a_normal_version(self):

        current_version = '1.2.3'

        suggested_version = tasks._suggest_version(current_version, tasks.PATCH_TAG)

        assert suggested_version == '1.2.4'

    def test_suggest_version_is_correct_for_a_version_with_metadata(self):

        current_version = '1.2.3+meta.data'

        suggested_version = tasks._suggest_version(current_version, tasks.MINOR_TAG)

        assert suggested_version == '1.3.0'

    def test_suggest_version_is_correct_for_a_version_with_pre_release_and_metadata(self):

        current_version = '1.2.3-pre.release+meta.data'

        suggested_version = tasks._suggest_version(current_version, tasks.MAJOR_TAG)

        assert suggested_version == '2.0.0'

    def test_suggest_version_is_correct_for_major_version_zero_and_major_bump(self):

        current_version = '0.50.1'

        suggested_version = tasks._suggest_version(current_version, tasks.MAJOR_TAG)

        assert suggested_version == '0.51.0'

    def test_suggest_version_is_correct_for_major_version_zero_and_patch_bump(self):

        current_version = '0.50.1'

        suggested_version = tasks._suggest_version(current_version, tasks.PATCH_TAG)

        assert suggested_version == '0.50.2'
