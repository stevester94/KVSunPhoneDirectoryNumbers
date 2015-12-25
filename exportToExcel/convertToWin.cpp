#include <stdio.h>
#include <stdlib.h>
#include <sqlite3.h> 
#include <iostream>
#include <assert.h>

using namespace std;
//Global sqlite3 database object
sqlite3 *db;

static int blankCallBack(void *data, int argc, char **argv, char **azColName) {
   return 0;
}

void updateEntry(char* displayName, char* newAllLines) {
   char* query = new char[10000];
   int returnCode;
   char *zErrMsg = 0;

   query[0] = '\0';

   strcat(query, "UPDATE Entries SET allLines= \"");
   strcat(query, newAllLines);
   strcat(query, "\" WHERE displayName= \"");
   strcat(query, displayName);
   strcat(query, "\";");

   cout << "QUERY: " << query << endl;
   returnCode = sqlite3_exec(db, query, blankCallBack, NULL, &zErrMsg);
   if( returnCode != SQLITE_OK ){
      fprintf(stderr, "SQL error: %s\n", zErrMsg);
   }else{
      fprintf(stdout, "Operation done successfully\n");
   }

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

static int callback(void *data, int argc, char **argv, char **azColName){
   //Iterates through each column found in that record

   assert(argc == 2);//If have more than 2 args something went wrong, dont want to fuck the database

   char* displayName = argv[0];
   char* allLines = argv[1];

   cout << "RECORD: " << displayName << " :\n";

   char* convertedLines = convertNewLinesToWin(allLines);

   //DEBUG
   // for(int i = 0; i < strlen(convertedLines); i++) {
   //    char currentChar = convertedLines[i];

   //    if(currentChar == '\r')
   //       cout << "1";
   //    else if(currentChar == '\n')
   //       cout << "2";
   //    else
   //       cout << "0";
   // }

   updateEntry(displayName, convertedLines);

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

   /* Create SQL statement */
   query = "SELECT displayName, allLines from Entries";

   /* Execute SQL statement */
   rc = sqlite3_exec(db, query, callback, NULL, &zErrMsg);
   if( rc != SQLITE_OK ){
      fprintf(stderr, "SQL error: %s\n", zErrMsg);
      sqlite3_free(zErrMsg);
   }else{
      fprintf(stdout, "Operation done successfully\n");
   }
   sqlite3_close(db);

   return 0;
}








