#include<iostream>
#include <stdio.h>
#include <curl/curl.h>

#include "TFile.h"
#include "TTree.h"

int main( int argc, char ** argv )
{
    int status = 0; // success
    
    int ndata2read = 1;
    if( argc > 1 ) {
        ndata2read = atoi( argv[1] );
    }
    printf( "INFO: no. of data to be read: %i\n", ndata2read );
    
    char ofilename[128];
    if( argc > 2 ) {
        sprintf( argv[2], ofilename );
    }
    TFile * f = TFile::Open( ofilename, "RECREATE" );
    
    int ew_id               = -1;
    int ew_timestamp        = -1;
    float ew_volt           = -666.;
    float ew_temperature    = -666.;
    
    TTree * ntuple = new TTree( "data", "Arduino sensors data" );
    ntuple->Branch( "id",            &ew_id,            "id/I" );
    ntuple->Branch( "timestamp",     &ew_timestamp,     "timestamp/I" );
    ntuple->Branch( "volt",          &ew_volt,          "volt/F" );
    ntuple->Branch( "temperature",   &ew_temperature,   "temperature/F" );
    
    
    const char * wpage = "http://0.0.0.0:5000/get_data?nreadings=5";
    CURL * curl = curl_easy_init();
    if( !curl ) {
        printf( "ERROR: cannot initialize CURL object\n" );
        return 1;
    }
    curl_easy_setopt( curl, CURLOPT_URL, wpage );
    CURLcode res = curl_easy_perform( curl );
    
    // event loop
    
    f->Close();
    curl_easy_cleanup(curl);
    
    return status;
}