package org.osm.keypadmapper;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.PrintWriter;
import java.util.Date;

import junit.framework.Assert;
import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import org.osm.keypadmapper.R;

public class KeypadMapper extends Activity {
    private int ids[] = { R.id.button_0, R.id.button_1, R.id.button_2,
    		R.id.button_3, R.id.button_4, R.id.button_5, R.id.button_6,
    		R.id.button_7, R.id.button_8, R.id.button_9, R.id.button_C,
    		R.id.button_DEL, R.id.button_L, R.id.button_F, R.id.button_R
    };
    private int val = 0;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        for (int i = 0; i < 15; i++) {
          Button button = (Button) findViewById (ids[i]);
          button.setOnClickListener(new Button.OnClickListener() {
        	  private void Do (String s) {
        		  PrintWriter out = null;
        		  Date d = new Date ();
        		  try {
        			  out = new PrintWriter (new FileOutputStream (
        					  "/sdcard/keypadmapper", true));
        			  out.print (d.getTime());
            		  out.print (s);
            		  out.println (val);
        		  } catch (FileNotFoundException e) {
        			  Assert.assertNotNull ("Error writing the file!", out);
				} finally {
        			  if (out != null) out.close ();        			  
           			  Assert.assertNotNull ("Error writing the file!", out);
       		  }
    			  /*if (out == null) AlertDialog.Builder(mContext)
                  .setIcon(R.drawable.alert_dialog_icon)
                  .setTitle("Error writing file !")*/
                  /*.setPositiveButton(R.string.alert_dialog_ok, new DialogInterface.OnClickListener() {
                      public void onClick(DialogInterface dialog, int whichButton) {

                      }
                  }); */
                  //.create ();
    			  val = 0;        		  
        	  }
        	  public void onClick (View v) {
                  for (int j = 0; j < 10; j++) {
                	  if (v == findViewById (ids[j])) val = val * 10 + j;
                  }
                  if (v == findViewById (R.id.button_C)) val = 0;
                  if (v == findViewById (R.id.button_DEL)) val /= 10;
                  if (v == findViewById (R.id.button_L)) Do ("L");
                  if (v == findViewById (R.id.button_F)) Do ("F");
                  if (v == findViewById (R.id.button_R)) Do ("R");
                  TextView tw = (TextView) findViewById (R.id.text);
                  tw.setText (Integer.toString(val));
        	  }
          });
        }
    }
}