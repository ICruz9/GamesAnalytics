import { Component, ViewChild, OnInit } from '@angular/core';
import {MatPaginator} from '@angular/material/paginator';
import {MatSort} from '@angular/material/sort';
//import { SelectionModel } from '@angular/cdk/collections';
import {MatTableDataSource} from '@angular/material/table';
import data from '../../data/data.json';
//import * as data from '../../data/data.json';

export interface Game {
  game: string;
  date: string;
  review: string;
  discount: string;
  original:string;
  final: string;
  image: string;
  href: string;
  time: string;
  metascore: string;
}

console.log(data)

const GAMES_DATA: Game[] = data;

// const initialSelection = [];
// const allowMultiSelect = true;
// this.selection = new SelectionModel<Game>(allowMultiSelect, initialSelection);

@Component({
  selector: 'app-games',
  templateUrl: './games.component.html',
  styleUrls: ['./games.component.scss']
})
export class GamesComponent implements OnInit {

  displayedColumns: string[] = ['image', 'name', 'date', 'price', 'review', 'time', 'store'];
  dataSource = new MatTableDataSource<Game>(GAMES_DATA);
  @ViewChild(MatSort, {static: true}) sort: MatSort;
  @ViewChild(MatPaginator, {static: true}) paginator: MatPaginator;
  //@ViewChild(MatPaginator, {static: true}) paginator: MatPaginator;

  constructor() { }

  
  ngOnInit(): void {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
    //this.dataSource.selection = this.selection;
  }

  // /** Whether the number of selected elements matches the total number of rows. */
  // isAllSelected() {
  //   const numSelected = this.selection.selected.length;
  //   const numRows = this.dataSource.data.length;
  //   return numSelected == numRows;
  // }

  // /** Selects all rows if they are not all selected; otherwise clear selection. */
  // masterToggle() {
  //   this.isAllSelected() ?
  //       this.selection.clear() :
  //       this.dataSource.data.forEach(row => this.selection.select(row));
  // }

  applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  test(value: string){
    console.log(value);
    console.log("Ffffffffffffffffffffff");
    return "good";
  }
    



}

