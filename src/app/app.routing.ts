import {Routes} from '@angular/router';
import {GamesComponent} from './games/games.component';


export const ROUTES: Routes = [
    {
        path: '', redirectTo: 'games', pathMatch: 'full'
    },
    {
      path: 'games', component: GamesComponent
    }
];
