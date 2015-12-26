// When program encounters a \n in the allLines field in the database it swaps it with \r\n


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
vector<char**> rows;
vector<char*> queries;

static int blankCallBack(void *data, int argc, char **argv, char **azColName) {
   return 0;
}

void runQueries() {
   int returnCode;
   char* errorString = 0;
   static int callCount = 0;

   for(vector<char*>::iterator it = queries.begin(); it != queries.end(); it++) {
      char* query = *it;

      returnCode = sqlite3_exec(db, query, NULL, NULL, &errorString);

      if( returnCode != SQLITE_OK ){
         cout << "error\n";
         cout << query << endl;
         exit(1);
      } else 
         cout << "Success on: " << callCount << endl;

      callCount++;

   }
}

void generateQuery(char* displayName, char* newAllLines) {
   static int callCount = 0;
   int totalLength;

   char* UPDATE_CLAUSE = "UPDATE Entries SET allLines= \"";
   char* WHERE_CLAUSE = "\" WHERE displayName= \"";
   char* END_CLAUSE = "\";";
   char* query;

   totalLength = strlen(UPDATE_CLAUSE) + strlen(WHERE_CLAUSE) + strlen(END_CLAUSE) + strlen(displayName) + strlen(newAllLines) + 1;

   query = new char[totalLength];
   query[0] = '\0';

   strcat(query, UPDATE_CLAUSE);
   strcat(query, newAllLines);
   strcat(query, WHERE_CLAUSE);
   strcat(query, displayName);
   strcat(query, END_CLAUSE);

   queries.push_back(query);
}

//Called by the select statement, individual call for each record SELECT pulls
char* convertNewLinesToWin(char* inString) {
   int lenInString = strlen(inString);
   char* outString = new char[lenInString * 2]; //Be sure to deallocate this bitch

   int j = 0; //Counter for the position in the outstring

   for(int i = 0; i < lenInString; i++, j++) {
      char currentChar = inString[i];

      assert(currentChar != '\r'); //Don't want to start doubling up on carriage returns, unexpected behaviour

      if(currentChar == '\n') {
         outString[j] = '\r';
         j++;
         outString[j] = '\n';
      } else {
         outString[j] = currentChar;
      }
   }

   return outString;

}

//Pushes displayName and allLines to vector rows
static int callback(void *data, int argc, char **argv, char **azColName){
   //Iterates through each column found in that record
   char** row = new char*[2];


   char* displayName = new char[strlen(argv[0])+1];
   char* allLines = new char[strlen(argv[1])+1];

   strcpy(displayName, argv[0]);
   strcpy(allLines, argv[1]);

   row[0] = displayName;
   row[1] = allLines;

   rows.push_back(row);

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


   // Convert allLines in row accordingly and update entry in DB
   int callCount = 0;
   for(vector<char**>::iterator it = rows.begin(); it != rows.end(); it++, callCount++) {
      char* displayName;
      char* allLines;
      char* newAllLines;

      try {
         // cout << "dereferencing...\n";
         displayName = (*it)[0];
         allLines = (*it)[1];
      } catch(int e) {
         cout << "dereferencing failed\n";
         exit(1);
      }

      try {
         // cout << "converting...\n";
         newAllLines = convertNewLinesToWin(allLines);
      } catch(int e) {
         cout << "convert failed\n";
         exit(1);
      }

      try {
         // cout << "updating...\n";
         generateQuery(displayName, newAllLines);
      } catch(int e) {
         cout << "update failed\n";
         exit(1);
      }
   }

   //Run those fucking queries
   runQueries();


   sqlite3_close(db);

   return 0;
}








