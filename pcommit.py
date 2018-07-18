#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import check_output
from time import strftime, localtime
import sys


if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


__author__ = "Pouriya Jahanbakhsh"


global INIT_TYPE
INIT_TYPE = "init"  # Initial commits

global FIX_TYPE
FIX_TYPE = "fix"    # Fix bugs

global FEAT_TYPE
FEAT_TYPE = "feat"  # New features

global REF_TYPE
REF_TYPE = "ref"    # Refactors

global TEST_TYPE
TEST_TYPE = "test"  # Writing, fixing, refactoring test codes

global DOC_TYPE
DOC_TYPE = "doc"    # Change documentations

global BUILD_TYPE
BUILD_TYPE = "build" # Changing Makefiles, etc

global STYLE_TYPE
STYLE_TYPE = "style" # Fix indentation, line breaks, etc

global CI_TYPE
CI_TYPE = "ci"       # Editing file for Continuous Integration

global VERSION_TYPE
VERSION_TYPE = "ver" # Versioning

global COMMIT_TYPES
COMMIT_TYPES = [INIT_TYPE
               ,FIX_TYPE
               ,FEAT_TYPE
               ,REF_TYPE
               ,TEST_TYPE
               ,DOC_TYPE
               ,BUILD_TYPE
               ,STYLE_TYPE
               ,CI_TYPE
               ,VERSION_TYPE]


class CommitsParser:


	def __init__(self, skip_unknown_commits=True):
		self.skip_unknown_commits = skip_unknown_commits


	def get_commit_lines(self):
		output  = run_command(["git", "log", "--oneline"])
#		output  = run_command(["cat", "commits.log"]) # For test
		lines = []
		for line in output.splitlines():
			lines.append(line.split(" ", 1)[1]) # skip commit hash
		return lines


	def parse_commits(self, commit_lines):
		parsed_commits = []
		for commit_line in commit_lines:
			try:
				commit = Commit(commit_line)
				parsed_commits.append(commit)
			except Exception as error:
				if not self.skip_unknown_commits:
					print("Error: {}".format(error))
					exit(1)
				print("Warning: {}".format(error))
		return parsed_commits


	def save_commits(self, commits):
		data = {1: [None, []]}
		number = 1
		for commit in commits:
			if commit.type != VERSION_TYPE:
				data[number][1].append(commit)
			else: # i.e ver: 1.2.10
				data[number][0] = commit.short_description
				data[number][1].append(commit)
	
				number += 1
				data[number] = [None, []]
		
		self.commits = []
		index = 1
		while index <= number:
			if data[index][0]:
				self.commits.append(tuple(data[index]))
			index += 1
		return self.commits


	def main(self):
		commit_lines = self.get_commit_lines()
		commits      = self.parse_commits(commit_lines)
		self.save_commits(commits)


class ChangeLog(CommitsParser):


	def __init__(self, since, skip_unknown_commits=True):
		CommitsParser.__init__(self, skip_unknown_commits)
		self.since = since


	def handle_commits(self, version, commits):
		return


	def handle_end_of_commits(self):
		pass


	def main(self):
		commit_lines = self.get_commit_lines()
		commits      = self.parse_commits(commit_lines)
		self.save_commits(commits)

		if self.since:
			run_callback = False
		else:
			run_callback = True

		for commit in self.commits:
			if run_callback:
				self.handle_commits(commit[0], commit[1])
				continue
			if commit[0] == self.since:
				run_callback = True
				self.handle_commits(commit[0], commit[1])
		self.handle_end_of_commits()

class MarkDownChangeLogGenerator(ChangeLog):

	FILE_NAME = "CHANGELOG.md"

	def __init__(self
                ,since=None
                ,skip_unknown_commits=True
                ,include_fix=True
                ,include_feat=True
                ,include_ref=True
                ,include_test=True
                ,fix_include_long_description=True
                ,feat_include_long_description=True
                ,ref_include_long_description=True
                ,test_include_long_description=True
                ,fix_include_files=True
                ,feat_include_files=True
                ,ref_include_files=True
                ,test_include_files=True):
		ChangeLog.__init__(self, since, skip_unknown_commits)

		self.fd = open(self.FILE_NAME, 'w')

		self.include_fix  = include_fix
		self.include_feat = include_feat
		self.include_ref  = include_ref
		self.include_test = include_test
		self.fix_include_long_description  = fix_include_long_description
		self.feat_include_long_description = feat_include_long_description
		self.ref_include_long_description  = ref_include_long_description
		self.test_include_long_description = test_include_long_description
		self.fix_include_files  = fix_include_files
		self.feat_include_files = feat_include_files
		self.ref_include_files  = ref_include_files
		self.test_include_files = test_include_files
		 
		

	def handle_commits(self, version, commits):
		self.fd.write("### {}\n".format(version))
		fix = []
		feat = []
		ref = []
		test = []
		for commit in commits:
			if commit.type == FIX_TYPE:
				fix.append(commit)
			elif commit.type == FEAT_TYPE:
				feat.append(commit)
			elif commit.type == REF_TYPE:
				ref.append(commit)
			elif commit.type == TEST_TYPE:
				test.append(commit)

		if self.include_fix and fix:
			self.fd.write("* **Fix(es):**\n")
			for commit in fix:
				self.fd.write("    * {}  \n".format(commit.short_description))
				if self.fix_include_long_description and commit.long_description:
					self.fd.write("        >{}  \n\n".format(commit.long_description))
				if self.fix_include_files and commit.files:
					files = ""
					for file in commit.files:
						files += ", {}".format(file)
					self.fd.write("        Files changed: {}  \n".format(files[2:]))
		if self.include_feat and feat:
			self.fd.write("* **Feature(s):**\n")
			for commit in feat:
				self.fd.write("    * {}  \n".format(commit.short_description))
				if self.feat_include_long_description and commit.long_description:
					self.fd.write("        >{}  \n\n".format(commit.long_description))
				if self.feat_include_files and commit.files:
					files = ""
					for file in commit.files:
						files += ", {}".format(file)
					self.fd.write("        Files changed: {}  \n".format(files[2:]))
		if self.include_ref and ref:
			self.fd.write("* **Refactor(s):**\n")
			for commit in ref:
				self.fd.write("    * {}  \n".format(commit.short_description))
				if self.ref_include_long_description and commit.long_description:
					self.fd.write("        >{}  \n\n".format(commit.long_description))
				if self.ref_include_files and commit.files:
					files = ""
					for file in commit.files:
						files += ", {}".format(file)
					self.fd.write("        Files changed: {}  \n".format(files[2:]))
		if self.include_test and test:
			self.fd.write("* **Test improvment(s):**\n")
			for commit in test:
				self.fd.write("    * {}  \n".format(commit.short_description))
				if self.test_include_long_description and commit.long_description:
					self.fd.write("        >{}  \n\n".format(commit.long_description))
				if self.test_include_files and commit.files:
					files = ""
					for file in commit.files:
						files += ", {}".format(file)
					self.fd.write("        Files changed: {}  \n".format(files[2:]))


	def handle_end_of_commits(self):
		self.fd.write("\nGenerated at {}".format(strftime('%Y-%m-%d %H:%M', localtime())))
		self.fd.close()


class CommitChanges:

	def __init__(self):
		self.type              = self.get_type()
		self.short_description = self.get_short_description()
		self.files             = self.get_files()
		self.long_description  = self.get_long_description()

		commit = "{}: {}".format(self.type, self.short_description)
		if self.files:
			commit += "\nFiles: {}".format(self.files)
		if self.long_description:
			commit += "\n{}".format(self.long_description)
		run_command(["git", "commit", "-m", commit])


	def get_type(self):
		while True:
			text = raw_input("Insert commit type {}:".format(tuple(COMMIT_TYPES)))
			if text in COMMIT_TYPES:
				return text


	def get_short_description(self):
		while True:
			text = raw_input("Insert commit main description (between 10-65 characters):")
			if len(text) <= 65:
				return text


	def get_files(self):
		text = raw_input("Insert changed files separated by comma (Enter to skip):")
		if text.strip():
			return text
		return

	def get_long_description(self):
		text = raw_input("Insert commit long description (Enter to skip):")
		if text.strip():
			return text
		return


class Commit:


	def __init__(self, text):
		self.text = text

		(self.type,              text) = self.parse_type(text)
		(self.short_description, text) = self.parse_short_description(text)
		(self.files,             text) = self.parse_files(text)
		self.long_description          = self.parse_long_description(text)


	def parse_type(self, text):
		parsed_text = text.split(":", 1)
		commit_type = parsed_text[0]
		if commit_type not in COMMIT_TYPES:
			raise TypeError("unknown commit type {!r} in {!r}".format(commit_type, self.text))
		return (commit_type.strip(), parsed_text[1])


	def parse_short_description(self, text):
		parsed_text = text.split("\\n", 1)
		if len(parsed_text) == 1:
			return (parsed_text[0].strip(), "")
		return (parsed_text[0].strip(), parsed_text[1])


	def parse_files(self, text):
		parsed_text = text.split(":", 1)
		if parsed_text[0].lower() != "files":
			return ([], text)

		parsed_text = parsed_text[1].split("\\n", 1)
		files       = []
		for file in parsed_text[0].split(","):
			files.append(file.strip())

		if len(parsed_text) == 1:
			return (files, "")
		return (files, parsed_text[1])


	def parse_long_description(self, text):
		return text


def run_command(command):
	try:
		return check_output(command)
	except Exception as error:
		print("could not run command {!r} because of {}".format(" ".join(command), error))
		exit(1)


if __name__ == "__main__":
	from optparse import OptionParser

	optp = OptionParser()
	optp.add_option("-m"
                   ,"--message"
                   ,action="store_const"
                   ,const=True
                   ,help="Used to wrap a commit and run 'git commit -m'"
                   ,dest='m')

	optp.add_option("-c"
                   ,"--changelog"
                   ,action="store_const"
                   ,const=True
                   ,help="Used to generating changelog"
                   ,dest='changelog')
	optp.add_option("-s"
                   ,"--since"
                   ,help="Generate changelog since specified version name"
                   ,dest='since')
	optp.add_option("-n"
                   ,"--no-unknown-commits"
                   ,action="store_const"
                   ,const=False
                   ,help="Prints warnings and skips unknown commands"
                   ,dest='no_unknown_commits'
                   ,default=True)

	optp.add_option("--include-fix"
                   ,action="store_const"
                   ,const=True
                   ,help="When generating changelog, used to include commits with 'fix' type"
                   ,dest='include_fix'
                   ,default=True)
	optp.add_option("--fix-include-long-desc"
                   ,action="store_const"
                   ,const=True
                   ,help="When generating changelog and --include-fix is used, It also includes long description of commit"
                   ,dest='fix_include_long_description'
                   ,default=True)
	optp.add_option("--fix-include-files"
                   ,action="store_const"
                   ,const=True
                   ,help="When generating changelog and --include-fix is used, It also includes changed files for commit"
                   ,dest='fix_include_files'
                   ,default=True)

	optp.add_option("--include-feat"
                   ,action="store_const"
                   ,const=True
                   ,help="When generating changelog, used to include commits with 'feat' type"
                   ,dest='include_feat'
                   ,default=True)
	optp.add_option("--feat-include-long-desc"
                   ,action="store_const"
                   ,const=True
                   ,help="When generating changelog and --include-feat is used, It also includes long description of commit"
                   ,dest='feat_include_long_description'
                   ,default=True)
	optp.add_option("--feat-include-files"
                   ,action="store_const"
                   ,const=True
                   ,help="When generating changelog and --include-feat is used, It also includes changed files for commit"
                   ,dest='feat_include_files'
                   ,default=True)

	optp.add_option("--include-ref"
                   ,action="store_const"
                   ,const=True
                   ,help="When generating changelog, used to include commits with 'ref' type"
                   ,dest='include_ref'
                   ,default=True)
	optp.add_option("--ref-include-long-desc"
                   ,action="store_const"
                   ,const=True
                   ,help="When generating changelog and --include-ref is used, It also includes long description of commit"
                   ,dest='ref_include_long_description'
                   ,default=True)
	optp.add_option("--ref-include-files"
                   ,action="store_const"
                   ,const=True
                   ,help="When generating changelog and --include-ref is used, It also includes changed files for commit"
                   ,dest='ref_include_files'
                   ,default=True)

	optp.add_option("--include-test"
                   ,action="store_const"
                   ,const=True
                   ,help="When generating changelog, used to include commits with 'test' type"
                   ,dest='include_test'
                   ,default=True)
	optp.add_option("--test-include-long-desc"
                   ,action="store_const"
                   ,const=True
                   ,help="When generating changelog and --include-test is used, It also includes long description of commit"
                   ,dest='test_include_long_description'
                   ,default=True)
	optp.add_option("--test-include-files"
                   ,action="store_const"
                   ,const=True
                   ,help="When generating changelog and --include-test is used, It also includes changed files for commit"
                   ,dest='test_include_files'
                   ,default=True)

	opts, args = optp.parse_args()

	if opts.m:
		try: 
			CommitChanges()
		except KeyboardInterrupt:
			print()
		finally:
			exit(0)

	if opts.changelog:
		try:
			MarkDownChangeLogGenerator(since=opts.since
                                      ,skip_unknown_commits=opts.no_unknown_commits
                                      ,include_fix=opts.include_fix
                                      ,include_feat=opts.include_feat
                                      ,include_ref=opts.include_ref
                                      ,include_test=opts.include_test
                                      ,fix_include_long_description=opts.fix_include_long_description
                                      ,feat_include_long_description=opts.feat_include_long_description
                                      ,ref_include_long_description=opts.ref_include_long_description
                                      ,test_include_long_description=opts.test_include_long_description
                                      ,fix_include_files=opts.fix_include_files
                                      ,feat_include_files=opts.feat_include_files
                                      ,ref_include_files=opts.ref_include_files
                                      ,test_include_files=opts.test_include_files).main()
		except KeyboardInterrupt:
			print()
		finally:
			exit(0)
	optp.print_help()
