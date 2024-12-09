import { inject, Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, finalize, Observable, throwError } from 'rxjs';
import { endpoints } from './api_endpoints';
import { ToastrService } from 'ngx-toastr';
import { SharedService } from './shared.service';

@Injectable({
  providedIn: 'root'
})
export class UploadService {
  http: HttpClient = inject(HttpClient);
  toastr : ToastrService = inject(ToastrService);
  sharedService : SharedService = inject(SharedService);


  // View-Feedback-API
  uploadFile (file: File) : Observable<any> {
    const formData: FormData = new FormData();
    formData.append('file', file, file.name);

    const loadingToast = this.toastr.info('Uploading File...', 'Please wait', {
      disableTimeOut: true,
      closeButton: false,
      positionClass: 'toast-top-center'
    });

    return this.http.post(endpoints.VIEW_FEEDBACK_API, formData).pipe(

      catchError(error => {
        if (loadingToast) {
          this.toastr.clear();
        }
        this.toastr.error('Failed to Upload File', 'Error');

        console.log(error);
        return throwError(() => error);
      }),
      finalize(() => {
        if (loadingToast) {
          this.toastr.clear();
        }
      })
    );
  }

  // Upload Expectaions API
  uploadExpectaions (file: File) : Observable<any> {
    const formData: FormData = new FormData();
    formData.append('file', file, file.name);

    const loadingToast = this.toastr.info('Uploading File...', 'Please wait', {
      disableTimeOut: true,
      closeButton: false,
      positionClass: 'toast-top-center'
    });

    return this.http.post(endpoints.UPLOAD_EXPECTATIONS_API, formData).pipe(

      catchError(error => {
        if (loadingToast) {
          this.toastr.clear();
        }
        this.toastr.error('Failed to Upload File', 'Error');

        console.log(error);
        return throwError(() => error);
      }),
      finalize(() => {
        if (loadingToast) {
          this.toastr.clear();
        }
      })
    );
  }

  // Store Expectations Embeddings API
  storeExpectaions (path : string) : Observable<any> {


    const loadingToast = this.toastr.info('Storing embeddings...', 'Please wait', {
      disableTimeOut: true,
      closeButton: false,
      positionClass: 'toast-top-center'
    });

    return this.http.post(endpoints.STORE_EXPECTATIONS_API, {path}).pipe(

      catchError(error => {
        if (loadingToast) {
          this.toastr.clear();
        }
        this.toastr.error('Failed to Upload File', 'Error');

        console.log(error);
        return throwError(() => error);
      }),
      finalize(() => {
        if (loadingToast) {
          this.toastr.clear();
        }
      })
    );
  }


  // Summarize-Feedback-API
  summarizeFeedback (feedbacks: string[]) : Observable<any> {
    const loadingToast = this.toastr.info('Generating summarized response...', 'Please wait', {
      disableTimeOut: true,
      closeButton: false,
      positionClass: 'toast-top-center'
    });

    return this.http.post(endpoints.VANILLA_SUMMARY_API, {feedbacks}).pipe(

      catchError(error => {
        if (loadingToast) {
          this.toastr.clear();
        }
        this.toastr.error('Failed to Summarize Data', 'Error');

        console.log(error);
        return throwError(() => error);
      }),
      finalize(() => {
        if (loadingToast) {
          this.toastr.clear();
        }
      })
    );
  }


  // Expectaions-Summarize-Feedback-API
  expSummarizeFeedback (feedbacks: string[], empDetail : any) : Observable<any> {
    const loadingToast = this.toastr.info('Generating summarized response...', 'Please wait', {
      disableTimeOut: true,
      closeButton: false,
      positionClass: 'toast-top-center'
    });

    return this.http.post(endpoints.EXP_SUMMARY_API, {feedbacks, empDetail}).pipe(

      catchError(error => {
        if (loadingToast) {
          this.toastr.clear();
        }
        this.toastr.error('Failed to Summarize Data', 'Error');

        console.log(error);
        return throwError(() => error);
      }),
      finalize(() => {
        if (loadingToast) {
          this.toastr.clear();
        }
      })
    );
  }


  // Approve-Feedback-API
  approveSummary (empDetail : any, summary:string) : Observable<any> {
    const loadingToast = this.toastr.info('Approving Summary...', 'Please wait', {
      disableTimeOut: true,
      closeButton: false,
      positionClass: 'toast-top-center'
    });

    return this.http.post(endpoints.APPROVE_SUMMARY_API, { empDetail:empDetail, summary:summary}).pipe(

      catchError(error => {
        if (loadingToast) {
          this.toastr.clear();
        }
        this.toastr.error('Failed to Summarize Data', 'Error');

        console.log(error);
        return throwError(() => error);
      }),
      finalize(() => {
        if (loadingToast) {
          this.toastr.clear();
        }
      })
    );
  }


  // Export-Summarize-Feedback-API
  exportFeedback (file : File, selectedPrompt : number) : Observable<any> {
    const loadingToast = this.toastr.info('Summarization in progress...', 'Please wait', {
      disableTimeOut: true,
      closeButton: false,
      positionClass: 'toast-top-center'
    });

    const formData: FormData = new FormData();
    formData.append('file', file, file.name);
    formData.append('use_custom_prompt', selectedPrompt.toString());
    console.log("Entered in Service");


    return this.http.post(endpoints.EXPORT_SUMMARY_API, formData).pipe(

      catchError(error => {
        if (loadingToast) {
          this.toastr.clear();
        }
        this.toastr.error('Failed to Summarize Data', 'Error');
        console.log(error);
        return throwError(() => error);
      }),
      finalize(() => {
        if (loadingToast) {
          this.toastr.clear();
        }
      })
    );
  }

  // Downlpad-Summarize-Feedback-CSV-API
  downloadSummaryCSV () : Observable<any> {
    const loadingToast = this.toastr.info('Downloading...', 'Please wait', {
      disableTimeOut: true,
      closeButton: false,
      positionClass: 'toast-top-center'
    });

    return this.http.get(endpoints.DOWNLOAD_SUMMARY_CSV_API,  { responseType: 'blob' }).pipe(

      catchError(error => {
        if (loadingToast) {
          this.toastr.clear();
        }
        this.toastr.error('Failed to download', 'Error');
        console.log(error);
        return throwError(() => error);
      }),
      finalize(() => {
        if (loadingToast) {
          this.toastr.clear();
        }
      })
    );
  }

  // Custom-Summarize-Feedback-API
  customSummarizeFeedback (feedbacks: string[], prompt: string) : Observable<any> {
    const loadingToast = this.toastr.info('Generating custom prompt response...', 'Please wait', {
      disableTimeOut: true,
      closeButton: false,
      positionClass: 'toast-top-center'
    });

    const body = { feedbacks, prompt };
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });


    return this.http.post(endpoints.CUSTOM_SUMMARY_API, body, {headers}).pipe(
      catchError(error => {
        if (loadingToast) {
          this.toastr.clear();
        }
        this.toastr.error('Failed to Summarize Data', 'Error');

        console.log(error);
        return throwError(() => error);
      }),
      finalize(() => {
        if (loadingToast) {
          this.toastr.clear();
        }
      })
    );
  }


  // Employee-Overview-API
  getEmpSummarizedOverview () : Observable<any> {
    const loadingToast = this.toastr.info('Fetching Data...', 'Please wait', {
      disableTimeOut: true,
      closeButton: false,
      positionClass: 'toast-top-center'
    });
    let userName : string;
    this.sharedService.loggedIn.subscribe(data => {
      userName = data;
    })

    return this.http.get(endpoints.EMP_SUMMARIZED_API+`?manager=${userName}`).pipe(
      catchError(error => {
        if (loadingToast) {
          this.toastr.clear();
        }
        this.toastr.error('Failed to Upload File', 'Error');
        console.log(error);
        return throwError(() => error);
      }),
      finalize(() => {
        if (loadingToast) {
          this.toastr.clear();
        }
      })
    );
  }


  // Employee-Overview-API
  getAllFeedbacks () : Observable<any> {

    return this.http.get(endpoints.GET_FEEDBACKS_API).pipe(
      catchError(error => {

        this.toastr.error('Failed to fetch data', 'Error');
        console.log(error);
        return throwError(() => error);
      }),

    );
  }

  // GET_COLLECTIONS-API
  getAllCollections () : Observable<any> {

    return this.http.get(endpoints.GET_ALL_COLLECTIONS_API).pipe(
      catchError(error => {

        this.toastr.error('Failed to get collections', 'Error');
        console.log(error);
        return throwError(() => error);
      }),

    );
  }

  // GET_HR_FEEDBACKS-API
  getHRSummaries () : Observable<any> {
    return this.http.get(endpoints.GET_HR_FEEDBACKS_API).pipe(
      catchError(error => {
        console.log(error);
        return throwError(() => error);
      }),

    );
  }

  // Select Collection-API
  // Store Expectations Embeddings API
  selectCollection (collection_name : string) : Observable<any> {
    const loadingToast = this.toastr.info('Selecting Collection...', 'Please wait', {
      disableTimeOut: true,
      closeButton: false,
      positionClass: 'toast-top-right'
    });

    return this.http.post(endpoints.SELECT_COLLECTION_API, {collection_name:collection_name}).pipe(

      catchError(error => {
        if (loadingToast) {
          this.toastr.clear();
        }
        this.toastr.error('Failed to select collection', 'Error');

        console.log(error);
        return throwError(() => error);
      }),
      finalize(() => {
        if (loadingToast) {
          this.toastr.clear();
        }
      })
    );
  }

  // PROMPT_RAG_API
  promptRag (query : string) : Observable<any> {


    return this.http.post(endpoints.PROMPT_RAG_API, {query:query}).pipe(

      catchError(error => {

        this.toastr.error('Something went wrong', 'Error');

        console.log(error);
        return throwError(() => error);
      }),

    );
  }


}
