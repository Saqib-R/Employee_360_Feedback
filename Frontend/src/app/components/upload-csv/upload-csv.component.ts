import { Component, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { UploadService } from '../../services/upload.service';
import { ToastrService } from 'ngx-toastr';
import { SharedService } from '../../services/shared.service';
import { animate, style, transition, trigger } from '@angular/animations';

@Component({
  selector: 'app-upload-csv',
  templateUrl: './upload-csv.component.html',
  styleUrls: ['./upload-csv.component.css'],
  animations: [
    // Modal open and close animation
    trigger('fadeInOut', [
      transition('void => *', [
        style({
          transform: 'translateY(-100px)',
          opacity: 0
        }),
        animate('300ms ease-out', style({
          transform: 'translateY(0)',
          opacity: 1
        }))
      ]),
      transition('* => void', [
        animate('300ms ease-in', style({
          transform: 'translateY(100px)',
          opacity: 0
        }))
      ])
    ])
  ]
})
export class UploadCSVComponent {
    uploadService: UploadService = inject(UploadService);
    csvFile: File | null = null;
    expecFile: File | null = null;
    csvData: any[] | null = null;
    displayedData: any[] | null = null;
    searchTerm: string = '';
    searchCollTerm: string = '';
    showSuccessMessage = false;
    path : string;
    continue : boolean = false;
    toastr: ToastrService = inject(ToastrService);
    isLoading : boolean = false;
    uploadSuccess : boolean = false;
    selectedCollection: string = "";
    collectionOptions : any;
    isLoadingCollections = false;
    filteredCollOptions : any = null;
    selectedOption: any = null;
    isDropdownOpen = false;


    ngOnInit(): void {
      if (localStorage.getItem('csvData')) {
          this.csvData = JSON.parse(localStorage.getItem('csvData'));
          this.displayedData = this.csvData;
      }
      this.fetchCollections();

  }

    // Toggle dropdown visibility
    toggleDropdown(state: boolean) {
      this.isDropdownOpen = state;
      if (!state) {
        this.searchTerm = '';
      }
    }

    // Filter the collection options based on the search term
    filterOptions() {
      if (!this.searchCollTerm) {
        this.filteredCollOptions = this.collectionOptions;
      } else {
        this.filteredCollOptions = this.collectionOptions.filter(option =>
          option.name.toLowerCase().includes(this.searchCollTerm.toLowerCase())
        );
      }
    }


    onDropdownChange(event: any): void {
      const selectedValue = event.target.value;
      console.log(`Dropdown changed: ${selectedValue}`);
    }


    // Select a collection option
    selectOption(option: any) {
      this.selectedOption = option;
      this.searchCollTerm = option.name;

      this.uploadService.selectCollection(this.searchCollTerm).subscribe({
        next: (res) => {
          console.log(res);
          this.isDropdownOpen = false;
          this.toastr.success("Collection selected successfully.")

        },
        error: (err) => {
          console.log(err);
        }
      }
      );
    }


    // Fetch initial collection options from the backend
    fetchCollections() {
      this.isLoadingCollections = true;
      this.uploadService.getAllCollections().subscribe({
        next: (res) => {
          console.log(res);
          this.collectionOptions = res;
          this.filteredCollOptions = [...this.collectionOptions];

          this.isLoadingCollections = false;

        },
        error: (err) => {
          console.log(err);
          this.isLoadingCollections = false;
        }
      }
      );
    }

    onCollectionSearch(event) {
      const term = event.target.value
      if (term.length > 2) {
        this.isLoadingCollections = true;

      }
    }

    // Handle collection selection
    onCollectionSelect(selected: any) {
      console.log('Selected collection:', selected);
    }


    onFileChange(event: Event) {
        const target = event.target as HTMLInputElement;
        if (target.files) {
            this.csvFile = target.files[0];
            console.log(this.csvFile);
        }
    }

    onExpecFileChange(event: Event) {
      const target = event.target as HTMLInputElement;
      if (target.files) {
          this.expecFile = target.files[0];
          console.log(this.expecFile);
      }
  }

    onSubmit() {
      if (this.csvFile) {
          this.uploadService.uploadFile(this.csvFile).subscribe({
              next: (res) => {
                  console.log(res);

                  this.csvData = res;
                  setTimeout(() => {
                    this.toastr.success('File Uploaded', 'Success...👍', {
                        timeOut: 5000,
                    });
                }, 10);

                const fileInput = document.getElementById('formFile') as HTMLInputElement;
                if (fileInput) {
                  fileInput.value = '';
                }
                  this.displayedData = this.csvData;
                  localStorage.setItem('csvData', JSON.stringify(this.csvData));
                  this.closeModal('feedbackModal');
              },
              error: (err) => {
                  console.error(err);
                  setTimeout(() => {
                    this.toastr.error('Failed to upload file', 'Error...👎', {
                        timeOut: 5000,
                    });
                }, 10);
              },
          });
      }
  }

  wantToContinue(flag) {
    if(flag) {
      this.uploadService.storeExpectaions(this.path).subscribe({
        next: (res)=> {
          console.log(res);
          this.path = res
          setTimeout(() => {
            this.toastr.success('Embedding Stored', 'Success...👍', {
                timeOut: 5000,
            });
        }, 10);

        this.closeModal('expectationsModal');
        this.expecFile = null;
        this.isLoading = false;
        this.uploadSuccess = false;
        },
        error: (err) => {
          console.log(err);

        }
      })
    }else{
      this.closeModal("expectationsModal");
      this.expecFile = null;
      this.isLoading = false;
      this.uploadSuccess = false;
    }
  }

  expecFileSubmit() {
    if (this.expecFile) {
      this.isLoading = true;
      this.uploadSuccess = false;
        this.uploadService.uploadExpectaions(this.expecFile).subscribe({
            next: (res) => {
                console.log(res);
                this.path = res.path
                setTimeout(() => {
                  this.toastr.success('File Uploaded', 'Success...👍', {
                      timeOut: 5000,
                  });
                  this.isLoading = false;
                  this.uploadSuccess = true;
              }, 10);


              const fileInput = document.getElementById('formFile') as HTMLInputElement;
              if (fileInput) {
                fileInput.value = '';
              }
            },
            error: (err) => {
                console.error(err);
                setTimeout(() => {
                  this.toastr.error('Failed to upload file', 'Error...👎', {
                      timeOut: 5000,
                  });
              }, 10);
              this.isLoading = false;

            },
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
        this.displayedData = null;
        const fileInput = document.getElementById('formFile') as HTMLInputElement;
        if (fileInput) {
          fileInput.value = '';
        }
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

  // Function to open a modal
  openModal(modalId: string): void {
    const modal = document.getElementById(modalId);
    if (modal) {
      const bootstrapModal = new bootstrap.Modal(modal);
      bootstrapModal.show();
    }
  }

  // Function to close a modal
  closeModal(modalId: string): void {
    this.csvFile = null; // Reset the selected file
    const modal = document.getElementById(modalId);
    if (modal) {
      const bootstrapModal = bootstrap.Modal.getInstance(modal);
      if (bootstrapModal) {
        bootstrapModal.hide();
      }
    }
  }

}
