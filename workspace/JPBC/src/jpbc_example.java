import it.unisa.dia.gas.jpbc.*;
import it.unisa.dia.gas.plaf.jpbc.pairing.PairingFactory;

 

public class jpbc_example{
	public static void main(String[] args){
		System.out.println("HelloWorld!");
		Pairing pairing = PairingFactory.getPairing("params.properties");
		PairingFactory.getInstance().setUsePBCWhenPossible(true);
		Field Zr = pairing.getZr();  //return zr
		Field G1 = pairing.getG1();  //return g1
		Field G2 = pairing.getG2();  //return g2
		Field GT = pairing.getGT();  //return gt
		
		int degree = pairing.getDegree();
		
		Element element = Zr.newElement();
	}
}
