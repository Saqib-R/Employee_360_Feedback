import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
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
}
