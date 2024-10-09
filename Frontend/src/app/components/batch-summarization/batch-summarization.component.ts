import { Component, inject } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { UploadService } from '../../services/upload.service';

@Component({
  selector: 'app-batch-summarization',
  templateUrl: './batch-summarization.component.html',
  styleUrl: './batch-summarization.component.css'
})
export class BatchSummarizationComponent {
  fileSelected : any;
  fileName: string | null = null;
  isLoading = false;
  isSummarized = false;
  toastr : ToastrService = inject(ToastrService);
  uploadService : UploadService = inject(UploadService);
  selectedPrompt: number = null;

  prompts: string[] = [
    'Generated Summary',
    'Custom Generated Summary',
  ];

  ngOnChanges() {
    console.log(this.selectedPrompt);

  }

  // Triggered when a file is selected
  onFileSelect(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.fileSelected = file;
      this.fileName = file.name;
    }
  }
  // Triggered when a file is dropped
  onFileDrop(event: DragEvent) {
    event.preventDefault();
    const file = event.dataTransfer?.files[0];
    if (file) {
      this.fileSelected = file;
      this.fileName = file.name;
    }
  }
  // Prevents default behavior on dragover
  onDragOver(event: DragEvent) {
    event.preventDefault();
  }

  // Simulate summarization process
  summarizeFile() {

    // Simulating a delay for summarization
    // setTimeout(() => {
    //   this.toastr.success('Summarization Process Completed', 'Success...👍', {
    //     timeOut: 30000,
    //   });


    //   this.isLoading = false;
    //   this.isSummarized = true;

    // }, 3000);

    if (!this.fileSelected || this.selectedPrompt === null) {
      this.toastr.error('Please upload valid csv file and select prompt to use.')
      return;
    }

    if(this.fileSelected && this.selectedPrompt) {
      this.isLoading = true;
      this.isSummarized = false;
      console.log(this.selectedPrompt);

      this.uploadService.exportFeedback(this.fileSelected, this.selectedPrompt).subscribe({
        next : (res) => {
          this.toastr.success('Summarization Process Completed', 'Success...👍', {
            timeOut: 30000,
          });
          console.log(res);
          this.isLoading = false;
          this.isSummarized = true;
        },
        error : (err) => {
          console.log(err);
          this.isLoading = false;
          this.isSummarized = false;
        }
      })
    }
  }

  // Clear the selected file
  clearFile() {
    this.fileSelected = false;
    this.fileName = null;
    this.isSummarized = false;
    this.isLoading = false;
    this.selectedPrompt = null;
    localStorage.removeItem('cusSummary')
    localStorage.removeItem('summary')
  }

  // Export functionality
  exportCsv() {
    console.log('Exporting CSV...');
    this.uploadService.downloadSummaryCSV().subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'summarized_feedback.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      },
      error: (error) => {
        console.log(error);

      }
    }
  )}

}
