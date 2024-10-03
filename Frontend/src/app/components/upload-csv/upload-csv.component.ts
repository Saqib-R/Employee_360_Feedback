import { Component, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { UploadService } from '../../services/upload.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-upload-csv',
  templateUrl: './upload-csv.component.html',
  styleUrl: './upload-csv.component.css'
})
export class UploadCSVComponent {
  uploadService : UploadService = inject(UploadService);
    csvFile: File | null = null;
    csvData : any[] | null = null;
    data: any[] | null = null;
    toastr : ToastrService = inject(ToastrService);


  ngOnInit(): void {
    if(localStorage.getItem('csvData')) {
      this.data = JSON.parse(localStorage.getItem('csvData'));
    }
  }

  onFileChange(event) {
    this.csvFile = event.target.files[0];
    console.log(this.csvFile);
  }

  onSubmit() {
    if(this.csvFile) {
      this.uploadService.uploadFile(this.csvFile).subscribe({
        next : (res) => {
          this.toastr.success('File Uplaoded', 'Success...👍', {
            timeOut: 50000,
          });

          this.csvData = res;
        },
        error : (err) => {
          console.error(err);
        }
      })
    }
  }

  showData() {
    this.data = this.csvData;
    localStorage.setItem('csvData', JSON.stringify(this.data));
  }

  resetFile() {
    this.csvFile = null;
    this.data = null;
    localStorage.removeItem('csvData')
  }
}
