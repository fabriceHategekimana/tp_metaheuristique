use ndarray::prelude::*;
use rand::prelude::*;

fn randomize() -> () {
    let res = (1..20000000).map(|x| rand::random::<f64>())
        .all(|x| x <= 1_f64);
    println!("res: {:?}", res);

}

//fn algo() -> () {
    //let N = 2;
    //let t = 0;
//
    //let s = random();
    //let v = Array::zeros((N,));
//
    //let J = compute_fitness();
    //let J_best = min([Jbest, J]);
    //let b = s;
//
    //let Jg_best = min(J_best);
    //let bg = bt(argmin J_best);
//
//
    //// for each particle
    //let (r1, r2) = (randint, randint);
    //v = (w*v)+(c1*r1(b-s))+(c2*r2*(bg-s));
    //s = s+v;
//
    //t += 1;
//}

fn main(){
   randomize();
}
