import { Component, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { UploadService } from '../../services/upload.service';
import { ToastrService } from 'ngx-toastr';
import { SharedService } from '../../services/shared.service';

@Component({
  selector: 'app-upload-csv',
  templateUrl: './upload-csv.component.html',
  styleUrls: ['./upload-csv.component.css']
})
export class UploadCSVComponent {
    uploadService: UploadService = inject(UploadService);
    csvFile: File | null = null;
    csvData: any[] | null = null;
    displayedData: any[] | null = null; // Separate variable for filtered data
    searchTerm: string = '';
    toastr: ToastrService = inject(ToastrService);

    ngOnInit(): void {
        if (localStorage.getItem('csvData')) {
            this.csvData = JSON.parse(localStorage.getItem('csvData'));
            this.displayedData = this.csvData; // Initialize displayedData with csvData
        }
    }

    onFileChange(event: Event) {
        const target = event.target as HTMLInputElement;
        if (target.files) {
            this.csvFile = target.files[0];
            console.log(this.csvFile);
        }
    }

    onSubmit() {
        if (this.csvFile) {
            this.uploadService.uploadFile(this.csvFile).subscribe({
                next: (res) => {
                    this.csvData = res;
                    this.displayedData = this.csvData; // Reset displayedData after upload
                    localStorage.setItem('csvData', JSON.stringify(this.csvData));
                },
                error: (err) => {
                    console.error(err);
                },
                complete : () => {
                    this.toastr.success('File Uploaded', 'Success...👍', {
                        timeOut: 500000,
                    });
                }
            });
        }
    }

    showData() {
        this.displayedData = this.csvData;
        localStorage.setItem('csvData', JSON.stringify(this.displayedData));
    }

    resetFile() {
        this.csvFile = null;
        this.csvData = null;
        this.displayedData = null; // Reset displayed data too
        localStorage.removeItem('csvData');
    }

    onSearchChange() {
        const term = this.searchTerm.toLowerCase();
        console.log("DATA\n", this.csvData, "\nTERM\n", term);

        if (this.csvData) {
            this.displayedData = this.csvData.filter(employee =>
                employee.subject.toLowerCase().includes(term) ||
                employee.function_code.toLowerCase().includes(term) ||
                employee.job_title.toLowerCase().includes(term) ||
                employee.level.toLowerCase().includes(term)
            );

            // If the search term is empty, reset displayedData to the full csvData
            if (term === '') {
                this.displayedData = this.csvData;
            }
        }
        console.log(this.displayedData);
    }
}
