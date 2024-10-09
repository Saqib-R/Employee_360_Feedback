import { inject, Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, finalize, Observable, throwError } from 'rxjs';
import { endpoints } from './api_endpoints';
import { ToastrService } from 'ngx-toastr';

@Injectable({
  providedIn: 'root'
})
export class UploadService {
  http: HttpClient = inject(HttpClient);
  toastr : ToastrService = inject(ToastrService);


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

    return this.http.post(endpoints.VIEW_SUMMARY_API, {feedbacks}).pipe(

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

}
