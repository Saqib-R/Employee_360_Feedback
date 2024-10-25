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
  expSummarizeFeedback (feedbacks: string[], role : string) : Observable<any> {
    const loadingToast = this.toastr.info('Generating summarized response...', 'Please wait', {
      disableTimeOut: true,
      closeButton: false,
      positionClass: 'toast-top-center'
    });

    return this.http.post(endpoints.EXP_SUMMARY_API, {feedbacks, role}).pipe(

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

        this.toastr.error('Failed to Upload File', 'Error');
        console.log(error);
        return throwError(() => error);
      }),

    );
  }

}
