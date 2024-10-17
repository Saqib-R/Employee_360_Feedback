import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SharedService {

  private dataSource = new BehaviorSubject<any>(null);
  private questionNo = new BehaviorSubject<any>(null);
  private csvData = new BehaviorSubject<any>(null);
  private isLoggedIn = new BehaviorSubject<any>(null);
  employeeData = this.dataSource.asObservable();
  questionNu = this.questionNo.asObservable();
  csvDatas = this.csvData.asObservable();
  loggedIn = this.isLoggedIn.asObservable();

  constructor() { }

  empData(data: any) {
    this.dataSource.next(data);
  }
  queNo(question : any) {
    this.questionNo.next(question);
  }
  csvEmpData(data : any) {
    console.log(data);

    this.csvData.next(data);
  }

  loggedInInfo(data : any) {
    this.isLoggedIn.next(data);
  }

}
