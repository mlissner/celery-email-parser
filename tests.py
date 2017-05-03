import unittest

import glob

from parsers import get_task_path_and_exc, get_task_args_and_kwargs


class MyTestCase(unittest.TestCase):
    test_files = glob.glob('test_fixtures/*.eml')

    def test_sucking_out_task_path_and_exc(self):
        correct = {
            '1.eml': (
                'cl.citations.tasks.update_document',
                "'ResponseNotReady()'"
            ),
            '2.eml': (
                'cl.citations.tasks.update_document',
                '"OperationalError(\'FATAL:  remaining connection slots are reserved for non-replication superuser connections\\\\n\',)"'
            ),
            '3.eml': (
                'cl.search.tasks.add_or_update_items',
                r""""ResponseError(u'Command # 1 (SETEX celery-task-meta-6a5b616a-2ff4-4436-a93e-01688b3e1d79 3600 \\\\x80\\\\x02}q\\\\x01(U\\\\x06statusq\\\\x02U\\\\x07SUCCESSq\\\\x03U\\\\ttracebackq\\\\x04NU\\\\x06resultq\\\\x05NU\\\\x08childrenq\\\\x06]u.) of pipeline caused error: MISCONF Redis is configured to save RDB snapshots, but is currently not able to persist on disk. Commands that may modify the data set are disabled. Please check Redis logs for details about the error.',)"
                """.strip(),  # Necessary because string is a bitch to parse.
            ),
            '4.eml': (
                'cl.citations.tasks.update_document',
                '"OperationalError(\'FATAL:  the database system is shutting down\\\\n\',)"',
            ),
        }
        for file_path in self.test_files:
            file_name = file_path.rsplit('/', 1)[1]
            self.assertEqual(correct[file_name], get_task_path_and_exc(file_path))

    def test_getting_args_and_kwargs(self):
        correct = {
            '1.eml': (
                '(<Opinion: 3338472 - Malinowski v. Bio-Gen Torrington, Inc., No. Cv 93 0524432 (Aug. 17, 1994)>, False)',
                '{}',
            ),
            '2.eml': (
                '(<Opinion: 1442194 - Thomas v. McGrath>, False)',
                '{}',
            ),
            '3.eml': (
                """([<Opinion: 2312935 - Mauro v. Raymark Industries, Inc.>, <Opinion: 2312936 - Harkless v. SWEENY IND. SCH. DIST. OF SWEENY, TEXAS>, <Opinion: 2312937 - HONEYWELL INTERN. v. Hamilton Sundstrand Corp.>, <Opinion: 2312938 - CR Bard, Inc. v. Wordtronics Corp.>, <Opinion: 2312939 - State v. Schubert>, <Opinion: 2312940 - Holtz v. JEFFERSON SMURFIT CORP.>, <Opinion: 2312941 - Lund v. Affleck>, <Opinion: 2312942 - United States v. Hildenbrandt>, <Opinion: 2312943 - United States v. Sloan>, <Opinion: 2312944 - Riotto v. Van Houten>, <Opinion: 2312945 - Feliz v. Conway>, <Opinion: 2312946 - C & P TELEPHONE v. Comptroller>, <Opinion: 2312947 - Rochkind v. Reynolds Securities, Inc.>, <Opinion: 2312948 - State v. Corey>, <Opinion: 2312949 - Brodar v. McKinney>, <Opinion: 2312950 - Com. v. Neely>, <Opinion: 2312951 - United States v. Edelmann>, <Opinion: 2312952 - Downey v. Wells Sanitary Dist.>, <Opinion: 2312953 - Frank's Nursery Sales, Inc. v. American Nat. Ins. Co.> , <Opinion: 2312954 - EchoMail, Inc. v. American Exp. Co.>, <Opinion: 2312955 - Keane v. COM. DEPT. OF TRANSP.>, <Opinion: 2312956 - Scalafani v. Moore-McCormack Lines, Inc.>, <Opinion: 2312957 - Medtronic, Inc. v. Guidant Corp.>, <Opinion: 2312958 - Firestine v. Poverman>, <Opinion: 2312959 - Buckeye Forest Council v. US Forest Service>, <Opinion: 2312960 - In Re Japanese Electronic Products Antitrust Lit.>, <Opinion: 2312961 - Jones v. United Parcel Service, Inc.>, <Opinion: 2312962 - United States v. Fields>, <Opinion: 2312963 - Boylan v. State>, <Opinion: 2312964 - O'Neal v. Central States, Southeast and Southwest>, <Opinion: 2312965 - Concerned Residents of Buck Hill Falls v. Grant>, <Opinion: 2312966 - Zanville v. Garza>, <Opinion: 2312967 - Larkin v. Duncan>, <Opinion: 2312968 - Cobaugh v. Klick-Lewis, Inc.>, <Opinion: 2312969 - Toney v. Dept. of Public Welfare>, <Opinion: 2312970 - GET OUTDOORS II v. City of Lemon Grove, Cal.>, <Opinion: 2312971 - Adair v. Nashville Housing Authority>, <Opinion: 2312972 - Cardi Corp. v. State>, <Opinion: 2312973 - Royster v. Costco Wholesale Corp.>, <Opinion: 2312974 - Matter of CVS Pharmacy Wayne>, <Opinion: 2312975 - United States v. Rogers>, <Opinion: 2312976 - Schor v. Abbott Laboratories>, <Opinion: 2312977 - In Re Estate of Fike>, <Opinion: 2312978 - Big Sky Music v. Todd>, <Opinion: 2312979 - McDermott v. Hughley>, <Opinion: 2312980 - Carroll v. United of Omaha Life Ins. Co.>, <Opinion: 2312981 - Com. v. Gambal>, <Opinion: 2312982 - Hammond v. United States>, <Opinion: 2312983 - Palmer v. Monroe County Sheriff>, <Opinion: 2312984 - Davis v. Com.>], 'http://127.0.0.1:8983/solr/collection1')""",
                '{}',
            ),
            '4.eml': (
                None, None
            )
        }
        for file_path in self.test_files:
            file_name = file_path.rsplit('/', 1)[1]
            self.assertEqual(correct[file_name],
                             get_task_args_and_kwargs(file_path))


if __name__ == '__main__':
    unittest.main()
