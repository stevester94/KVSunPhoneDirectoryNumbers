//Will dump the whole database:
//	{Displayname}
//	{0 for char, 1 for Carriage return, 2 for new line}

//compile with g++ sanityCheck.cpp -l sqlite3

#include <stdio.h>
#include <stdlib.h>
#include <sqlite3.h> 
#include <iostream>
#include <assert.h>
#include <vector>

using namespace std;
//Global sqlite3 database object
sqlite3 *db;

static int callback(void *data, int argc, char **argv, char **azColName) {
	char* displayName = argv[0];
	char* allLines = argv[1];

	cout << displayName << " :\n";

	for(int i = 0; i < strlen(allLines); i++) {
		if(allLines[i] == '\r')
			cout << "1";
		else if(allLines[i] == '\n')
			cout << "2";
		else
			cout << "0";
	}

	cout << endl << endl;

	return 0;
}

int main(int argc, char* argv[])
{
   char *zErrMsg = 0;
   int rc;
   char *query;

   /* Open database */
   rc = sqlite3_open("entries.db", &db);
   if( rc ){
      fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
      exit(0);
   }else{
      fprintf(stderr, "Opened database successfully\n");
   }

   //Populate the row vector
   query = "SELECT displayName, allLines from Entries";
   rc = sqlite3_exec(db, query, callback, NULL, &zErrMsg);
   if( rc != SQLITE_OK ){
      fprintf(stderr, "SQL error: %s\n", zErrMsg);
      sqlite3_free(zErrMsg);
   }else{
      fprintf(stdout, "Select executed successfully\n");
   }

}