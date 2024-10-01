import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, finalize, Observable, throwError } from 'rxjs';
import { endpoints } from './api_endpoints';

@Injectable({
  providedIn: 'root'
})
export class UploadService {
  http: HttpClient = inject(HttpClient);

  // View-Feedback-API
  uploadFile (file: File) : Observable<any> {
    const formData: FormData = new FormData();
    formData.append('file', file, file.name);

    return this.http.post(endpoints.VIEW_FEEDBACK_API, formData).pipe(
      catchError(error => {
        console.log(error);
        return throwError(() => error);
      })
    );
  }
}
